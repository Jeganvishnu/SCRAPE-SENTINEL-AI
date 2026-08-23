import uuid
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger_config import logger
from app.models.ai_diagnosis import AIDiagnosis
from app.ai.providers.mock_provider import MockAIProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.google_provider import GoogleGeminiProvider
from app.ai.context_builder import context_builder
from app.ai.repair_planner import repair_planner
from app.ai.safety_gate import safety_gate

class DiagnosisService:
    def get_provider(self):
        prov = settings.AI_PROVIDER.lower()
        if prov == "google" or prov == "gemini":
            return GoogleGeminiProvider()
        elif prov == "openai":
            return OpenAIProvider()
        else:
            return MockAIProvider()

    def diagnose_and_plan(self, db: Session, failure_event_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        # 1. Build failure context
        ctx = context_builder.build_context(db, failure_event_id)
        if not ctx:
            logger.warning(f"Failure context for event '{failure_event_id}' not found.")
            return None

        # 2. Select AI Provider
        provider = self.get_provider()

        # 3. Analyze failure with AI provider (or safe fallback)
        try:
            raw_diag = provider.analyze_failure(ctx)
        except Exception as e:
            logger.error(f"AI provider failed during failure analysis: {e}. Using MockAIProvider fallback.")
            raw_diag = MockAIProvider().analyze_failure(ctx)

        # 4. Generate repair plan
        raw_plan = provider.generate_repair_plan(raw_diag, ctx)
        structured_plan = repair_planner.generate_plan(raw_plan, ctx)

        # 5. Evaluate through Safety Gate
        gate_res = safety_gate.evaluate(structured_plan, ctx)

        # 6. Persist AI reasoning metadata to database
        db_diag = AIDiagnosis(
            source_id=uuid.UUID(ctx["source_id"]),
            failure_event_id=failure_event_id,
            model=settings.AI_MODEL if settings.AI_PROVIDER != "mock" else "mock",
            prompt_version=settings.AI_PROMPT_VERSION,
            failure_category=raw_diag.get("failure_category", "unknown"),
            confidence=raw_diag.get("confidence", 0.0),
            root_cause=raw_diag.get("root_cause", "Extraction failure detected."),
            evidence=raw_diag.get("evidence", []),
            repair_type=structured_plan["repair_type"],
            repair_plan=structured_plan,
            risk=gate_res["risk"],
            approved=gate_res["approved"],
            requires_manual_review=gate_res["requires_manual_review"],
            verification_status="pending"
        )
        db.add(db_diag)
        db.commit()
        db.refresh(db_diag)

        return {
            "id": str(db_diag.id),
            "source_id": ctx["source_id"],
            "failure_event_id": ctx["failure_event_id"],
            "model": db_diag.model,
            "prompt_version": db_diag.prompt_version,
            "failure_category": db_diag.failure_category,
            "confidence": float(db_diag.confidence),
            "root_cause": db_diag.root_cause,
            "evidence": db_diag.evidence,
            "repair_type": db_diag.repair_type,
            "repair_plan": db_diag.repair_plan,
            "risk": db_diag.risk,
            "approved": db_diag.approved,
            "requires_manual_review": db_diag.requires_manual_review,
            "verification_status": db_diag.verification_status,
            "reasons": gate_res["reasons"],
            "created_at": db_diag.created_at.isoformat()
        }

    def get_history(self, db: Session, source_id: Optional[uuid.UUID] = None, limit: int = 50) -> List[Dict[str, Any]]:
        query = db.query(AIDiagnosis)
        if source_id:
            query = query.filter(AIDiagnosis.source_id == source_id)

        rows = query.order_by(AIDiagnosis.created_at.desc()).limit(limit).all()
        result = []
        for r in rows:
            result.append({
                "id": str(r.id),
                "source_id": str(r.source_id),
                "failure_event_id": str(r.failure_event_id),
                "model": r.model,
                "prompt_version": r.prompt_version,
                "failure_category": r.failure_category,
                "confidence": float(r.confidence),
                "root_cause": r.root_cause,
                "evidence": r.evidence,
                "repair_type": r.repair_type,
                "repair_plan": r.repair_plan,
                "risk": r.risk,
                "approved": r.approved,
                "requires_manual_review": r.requires_manual_review,
                "verification_status": r.verification_status,
                "created_at": r.created_at.isoformat()
            })
        return result

diagnosis_service = DiagnosisService()
