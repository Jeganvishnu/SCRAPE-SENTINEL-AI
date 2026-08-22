import pytest
import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.source import Source
from app.models.scrape_run import ScrapeRun
from app.models.scraped_record import ScrapedRecord
from app.models.validation_result import ValidationResult
from app.models.failure_event import FailureEvent

# In-memory SQLite for rapid offline unit testing
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

def test_source_creation(db_session):
    src = Source(
        name="Test Target",
        url="https://example.com/changelog",
        collector_id="c_test123",
        status="active"
    )
    db_session.add(src)
    db_session.commit()

    saved = db_session.query(Source).filter_by(collector_id="c_test123").first()
    assert saved is not None
    assert saved.name == "Test Target"
    assert saved.status == "active"

def test_full_pipeline_persistence(db_session):
    # 1. Create Source
    src = Source(name="Supabase Test", url="https://supabase.com/changelog", collector_id="c_mt46lngz2asqzj8tkj")
    db_session.add(src)
    db_session.commit()

    # 2. Create ScrapeRun
    run = ScrapeRun(source_id=src.id, collector_id=src.collector_id, status="success", records_found=10, records_valid=10)
    db_session.add(run)
    db_session.commit()

    # 3. Create ScrapedRecord
    rec = ScrapedRecord(
        source_id=src.id,
        scrape_run_id=run.id,
        title="v2.1.0 Released",
        url="https://supabase.com/changelog/v2-1-0",
        content_hash="a" * 64,
        scraped_at=datetime.now(timezone.utc)
    )
    db_session.add(rec)

    # 4. Create ValidationResult
    val = ValidationResult(
        scrape_run_id=run.id,
        validation_status="passed",
        schema_valid=True,
        required_fields_valid=True,
        url_valid=True,
        date_valid=True,
        duplicate_free=True,
        record_count_valid=True,
        schema_change_detected=False,
        validation_score=100.0
    )
    db_session.add(val)

    # 5. Create FailureEvent
    fail = FailureEvent(
        source_id=src.id,
        scrape_run_id=run.id,
        failure_type="schema_change",
        severity="medium",
        message="Test warning schema drift"
    )
    db_session.add(fail)
    db_session.commit()

    # Assert relations
    assert len(src.runs) == 1
    assert len(run.records) == 1
    assert run.validation.validation_score == 100.0
    assert len(src.failures) == 1
