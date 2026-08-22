import logging as std_logging
import sys

def setup_logging():
    std_logging.basicConfig(
        level=std_logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        handlers=[
            std_logging.StreamHandler(sys.stdout)
        ]
    )
    logger = std_logging.getLogger("scrape_sentinel")
    logger.info("Structured logging initialized for Scrape Sentinel AI.")
    return logger

logger = setup_logging()
