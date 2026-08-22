import pytest
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base
from app.models.source import Source
from app.models.scrape_run import ScrapeRun
from app.models.validation_result import ValidationResult
from app.models.failure_event import FailureEvent
from app.models.healing_attempt import HealingAttempt

from app.services.health_service import health_service
from app.services.metrics_service import metrics_service
from main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

def test_health_score_calculation(db_session):
    src = Source(name="Test Source", url="https://example.com", collector_id="c_test1")
    db_session.add(src)
    db_session.commit()

    # Add 9 success runs + 1 failed run
    now = datetime.now(timezone.utc)
    for i in range(9):
        run = ScrapeRun(source_id=src.id, collector_id=src.collector_id, status="success", started_at=now - timedelta(hours=i))
        db_session.add(run)
        db_session.commit()

        val = ValidationResult(scrape_run_id=run.id, validation_status="passed", schema_valid=True, required_fields_valid=True, url_valid=True, date_valid=True, duplicate_free=True, record_count_valid=True, schema_change_detected=False, validation_score=100.0)
        db_session.add(val)

    failed_run = ScrapeRun(source_id=src.id, collector_id=src.collector_id, status="failed", started_at=now)
    db_session.add(failed_run)
    db_session.commit()

    score, state, explanation = health_service.calculate_health_score_and_state(db_session, source_id=src.id, period="7d")
    assert score > 70.0
    assert state in ("healthy", "warning", "degraded")
    assert "success rate" in explanation.lower() or "score" in explanation.lower()

def test_recovery_rate_and_mttr(db_session):
    src = Source(name="Recovery Test Source", url="https://example.com", collector_id="c_rec1")
    db_session.add(src)
    db_session.commit()

    run = ScrapeRun(source_id=src.id, collector_id=src.collector_id, status="failed")
    db_session.add(run)
    db_session.commit()

    fail = FailureEvent(source_id=src.id, scrape_run_id=run.id, failure_type="schema_change", severity="high", message="Drift detected")
    db_session.add(fail)
    db_session.commit()

    now = datetime.now(timezone.utc)
    h1 = HealingAttempt(
        source_id=src.id,
        scrape_run_id=run.id,
        failure_event_id=fail.id,
        collector_id=src.collector_id,
        attempt_number=1,
        started_at=now - timedelta(seconds=300),
        completed_at=now,
        status="verified"
    )
    db_session.add(h1)
    db_session.commit()

    rec_rate, mttr = health_service.calculate_recovery_metrics(db_session, source_id=src.id)
    assert rec_rate == 100.0
    assert mttr == 300.0

def test_empty_database_metrics(db_session):
    overview = metrics_service.get_overview_metrics(db_session, period="7d")
    assert overview["total_sources"] == 0
    assert overview["total_runs"] == 0
    assert overview["success_rate"] == 100.0
    assert overview["recovery_rate"] is None
    assert overview["mttr_seconds"] is None

def test_readiness_and_status_endpoints():
    client = TestClient(app)
    r_ready = client.get("/ready")
    assert r_ready.status_code == 200
    assert r_ready.json()["status"] == "ready"

    r_sys = client.get("/system/status")
    assert r_sys.status_code == 200
    assert r_sys.json()["database"] == "connected"
