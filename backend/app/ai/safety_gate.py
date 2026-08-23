from typing import Dict, Any
from app.core.config import settings

class SafetyGate:
    """
    AI Safety Gate & Policy Enforcement Engine.
    Rules:
    - LOW Risk + High Confidence (>= 0.85) + Allowed Repair -> Approved for automated Phase 5 healing.
    - MEDIUM Risk OR Medium Confidence (0.65 - 0.8499) -> Requires Manual Review.
    - HIGH Risk OR Low Confidence (< 0.65) OR Disallowed Repair -> Blocked / Manual Review.
    - Loop Protection: Exceeding max 3 repair attempts forces Manual Review.
    """

    def evaluate(self, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        conf = float(plan.get("confidence", 0.0))
        risk = plan.get("risk", "high").lower()
        allowed = plan.get("allowed", True)
        attempts = context.get("healing_attempts_count", 0)

        reasons = []
        approved = False
        requires_manual_review = True

        # Check repair loop limit
        if attempts >= settings.AI_MAX_REPAIR_ATTEMPTS:
            reasons.append(f"Repair attempt limit ({settings.AI_MAX_REPAIR_ATTEMPTS}) reached for this failure.")
            risk = "high"

        # Safety boundary evaluation
        if not allowed:
            reasons.append("Repair type is disallowed by Safety Gate policy.")
            risk = "blocked"
        elif attempts >= settings.AI_MAX_REPAIR_ATTEMPTS:
            reasons.append("Forced manual review due to repeated repair attempts.")
        elif conf >= settings.AI_HIGH_CONFIDENCE_THRESHOLD and risk == "low":
            approved = True
            requires_manual_review = False
            reasons.append("High confidence diagnosis with low risk repair plan.")
        elif conf >= settings.AI_MEDIUM_CONFIDENCE_THRESHOLD or risk == "medium":
            reasons.append("Medium confidence or medium risk repair requires manual human review.")
        else:
            reasons.append("Low confidence diagnosis or high risk plan requires manual inspection.")

        return {
            "approved": approved,
            "risk": risk,
            "reasons": reasons,
            "requires_manual_review": requires_manual_review
        }

safety_gate = SafetyGate()
