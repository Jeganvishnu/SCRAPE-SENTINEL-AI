import json
import subprocess
import shutil
from typing import Any, Dict, List, Optional
from app.core.brightdata_config import brightdata_settings
from app.core.logger_config import logger

class BrightDataError(Exception):
    """Base exception for Bright Data integration errors."""
    pass

class BrightDataCLINotFoundError(BrightDataError):
    pass

class BrightDataAuthError(BrightDataError):
    pass

class CollectorNotFoundError(BrightDataError):
    pass

class ScraperRunFailedError(BrightDataError):
    pass

class ScraperEmptyResultError(BrightDataError):
    pass

class ScraperInvalidOutputError(BrightDataError):
    pass

class ScraperTimeoutError(BrightDataError):
    pass


class BrightDataService:
    def __init__(self, timeout_seconds: int = 120):
        self.timeout_seconds = timeout_seconds
        self._cli_path = shutil.which("brightdata") or shutil.which("bdata")

    def _verify_cli(self) -> str:
        if not self._cli_path:
            raise BrightDataCLINotFoundError(
                "Bright Data CLI ('brightdata' or 'bdata') was not found on system PATH."
            )
        return self._cli_path

    def get_collector_id(self) -> str:
        collector_id = brightdata_settings.BRIGHT_DATA_COLLECTOR_ID
        if not collector_id:
            raise CollectorNotFoundError("BRIGHT_DATA_COLLECTOR_ID is not set in environment or .env file.")
        return collector_id

    def create_collector(self, target_url: str, description: str, name: str = "scrape-sentinel-primary") -> Dict[str, Any]:
        cli = self._verify_cli()
        
        # Safe argument array execution (no shell string concatenation)
        cmd = [
            cli,
            "scraper",
            "create",
            target_url,
            description,
            "--name", name
        ]

        logger.info(f"Invoking Bright Data CLI scraper create for target URL: {target_url}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False
            )
        except subprocess.TimeoutExpired:
            raise ScraperTimeoutError(f"Bright Data scraper create timed out after {self.timeout_seconds}s.")
        except Exception as e:
            raise ScraperRunFailedError(f"Subprocess execution error during scraper create: {str(e)}")

        if result.returncode != 0:
            err_msg = result.stderr.strip() or result.stdout.strip()
            if "No API key found" in err_msg or "unauthorized" in err_msg.lower():
                raise BrightDataAuthError("Bright Data CLI authentication failed: missing or invalid API key.")
            raise ScraperRunFailedError(f"Bright Data scraper creation failed: {err_msg}")

        try:
            output_data = json.loads(result.stdout.strip())
            return output_data
        except json.JSONDecodeError:
            # Fallback if raw text output returned with collector_id
            output_text = result.stdout.strip()
            return {"raw_output": output_text, "status": "completed"}

    def run_collector(self, collector_id: str, target_url: Optional[str] = None) -> List[Dict[str, Any]]:
        cli = self._verify_cli()

        if not collector_id or not collector_id.startswith("c_"):
            raise CollectorNotFoundError(f"Invalid Collector ID format: '{collector_id}'. Expected 'c_...'.")

        cmd = [
            cli,
            "scraper",
            "run",
            collector_id
        ]
        if target_url:
            cmd.append(target_url)

        logger.info(f"Executing Bright Data scraper run for Collector ID: {collector_id}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False
            )
        except subprocess.TimeoutExpired:
            raise ScraperTimeoutError(f"Bright Data scraper run timed out after {self.timeout_seconds}s.")
        except Exception as e:
            raise ScraperRunFailedError(f"Subprocess execution error during scraper run: {str(e)}")

        if result.returncode != 0:
            err_msg = result.stderr.strip() or result.stdout.strip()
            if "No API key" in err_msg or "unauthorized" in err_msg.lower():
                raise BrightDataAuthError("Bright Data CLI authentication failed.")
            if "not found" in err_msg.lower():
                raise CollectorNotFoundError(f"Collector '{collector_id}' not found: {err_msg}")
            raise ScraperRunFailedError(f"Bright Data scraper execution failed: {err_msg}")

        raw_stdout = result.stdout.strip()
        if not raw_stdout:
            raise ScraperEmptyResultError("Bright Data scraper returned empty stdout output.")

        try:
            parsed_data = json.loads(raw_stdout)
            if isinstance(parsed_data, dict):
                # If wrapped in a single record or envelope object
                if "records" in parsed_data and isinstance(parsed_data["records"], list):
                    records = parsed_data["records"]
                elif "data" in parsed_data and isinstance(parsed_data["data"], list):
                    records = parsed_data["data"]
                else:
                    records = [parsed_data]
            elif isinstance(parsed_data, list):
                records = parsed_data
            else:
                raise ScraperInvalidOutputError(f"Unexpected JSON structure returned from scraper: {type(parsed_data)}")

            if not records:
                raise ScraperEmptyResultError("Bright Data scraper returned 0 extracted records.")

            return records

        except json.JSONDecodeError as e:
            raise ScraperInvalidOutputError(f"Failed to parse Bright Data scraper JSON output: {str(e)}")

brightdata_service = BrightDataService()
