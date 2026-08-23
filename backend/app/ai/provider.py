from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    @abstractmethod
    def analyze_failure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes scraper failure context and returns structured diagnosis:
        {
            "failure_category": "...",
            "confidence": 0.0-1.0,
            "root_cause": "...",
            "evidence": [...],
            "affected_fields": [...],
            "severity": "...",
            "recommended_action": "..."
        }
        """
        pass

    @abstractmethod
    def generate_repair_plan(self, diagnosis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured repair plan:
        {
            "repair_type": "...",
            "target": "...",
            "changes": [...],
            "reason": "...",
            "confidence": 0.0-1.0,
            "risk": "low"|"medium"|"high"|"blocked",
            "verification_required": True
        }
        """
        pass
