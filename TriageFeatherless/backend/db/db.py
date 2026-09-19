import os
from datetime import datetime, timezone

import psycopg
from psycopg import sql

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    Text,
    create_engine,
    delete,
    func,
    select,
    text,
    update,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)
from sqlalchemy.engine import make_url

from app.models.patient import PatientData
from app.models.triage_result import TriageResult
from app.models.triage_response import AIAssessment


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATABASE_URL = os.environ["DATABASE_URL"]

# Patient workflow states used by the triage board.
STATUS_WAITING = "waiting"
STATUS_IN_TREATMENT = "in_treatment"
STATUS_DONE = "done"

VALID_STATUSES = {
    STATUS_WAITING,
    STATUS_IN_TREATMENT,
    STATUS_DONE,
}


# --------------------------------------------------
# SQLAlchemy base
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


# --------------------------------------------------
# Patient table
# --------------------------------------------------

class Patient(Base):
    """
    A single triage encounter.

    One row is created every time a patient is assessed through the
    main ``/triage`` endpoint. The deterministic triage result is
    stored alongside the raw patient data so that the dashboard and
    the triage board can sort and display patients by urgency without
    re-running the engine.
    """

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # ---- Patient data ---------------------------------------------

    name: Mapped[str | None] = mapped_column(Text, nullable=True)

    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    symptoms: Mapped[list] = mapped_column(JSON, nullable=False)

    vital_signs: Mapped[dict] = mapped_column(JSON, nullable=False)

    clinical_context: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    # ---- Deterministic triage result ------------------------------

    triage_group: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    treatment_priority: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    color: Mapped[str | None] = mapped_column(Text, nullable=True)

    max_wait_minutes: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    reevaluation_minutes: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    red_flags: Mapped[list | None] = mapped_column(
        JSON, nullable=True
    )

    relevant_factors: Mapped[list | None] = mapped_column(
        JSON, nullable=True
    )

    requires_human_review: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # Full serialized triage result for the detail view.
    triage_result: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )

    # ---- Independent AI assessment --------------------------------

    ai_severity: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    ai_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    ai_explanation: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    # ---- Workflow -------------------------------------------------

    status: Mapped[str] = mapped_column(
        Text, nullable=False, default=STATUS_WAITING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        onupdate=func.now(),
    )


# --------------------------------------------------
# Engine (shared, module level)
# --------------------------------------------------

_engine = create_engine(DATABASE_URL, future=True)


def get_engine():
    return _engine


# --------------------------------------------------
# Database creation
# --------------------------------------------------

def create_database_if_not_exists():
    """
    Creates the PostgreSQL database specified in DATABASE_URL
    if it does not already exist.
    """

    url = make_url(DATABASE_URL)

    database_name = url.database

    if not database_name:
        raise RuntimeError(
            "DATABASE_URL does not contain a database name."
        )

    with psycopg.connect(
        host=url.host,
        port=url.port,
        dbname="postgres",
        user=url.username,
        password=url.password,
        autocommit=True,
    ) as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (database_name,),
            )

            if not cursor.fetchone():
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(database_name)
                    )
                )
                print(f"Database '{database_name}' created.")
            else:
                print(f"Database '{database_name}' already exists.")


# --------------------------------------------------
# Table creation + lightweight migration
# --------------------------------------------------

# Columns added after the very first schema. Applied idempotently so
# an existing "patients" table is upgraded in place without dropping
# any data.
_MIGRATION_COLUMNS = {
    "name": "TEXT",
    "triage_group": "INTEGER",
    "treatment_priority": "TEXT",
    "color": "TEXT",
    "max_wait_minutes": "INTEGER",
    "reevaluation_minutes": "INTEGER",
    "red_flags": "JSON",
    "relevant_factors": "JSON",
    "requires_human_review": "BOOLEAN DEFAULT TRUE",
    "triage_result": "JSON",
    "ai_severity": "INTEGER",
    "ai_reason": "TEXT",
    "ai_explanation": "TEXT",
    "status": "TEXT DEFAULT 'waiting'",
    "created_at": "TIMESTAMPTZ DEFAULT NOW()",
    "updated_at": "TIMESTAMPTZ DEFAULT NOW()",
}


def create_tables():
    """Creates missing tables and adds any missing columns."""

    Base.metadata.create_all(_engine)

    with _engine.begin() as connection:
        for column, definition in _MIGRATION_COLUMNS.items():
            connection.execute(
                text(
                    f"ALTER TABLE patients "
                    f"ADD COLUMN IF NOT EXISTS {column} {definition}"
                )
            )

    print("Database tables initialized.")


def initialize_database():
    """Ensures the database and all tables/columns exist."""

    create_database_if_not_exists()
    create_tables()


# --------------------------------------------------
# Serialization
# --------------------------------------------------

def _serialize(patient: Patient) -> dict:
    """Converts a Patient row into a JSON-friendly dict."""

    return {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "symptoms": patient.symptoms,
        "vital_signs": patient.vital_signs,
        "clinical_context": patient.clinical_context,
        "triage_group": patient.triage_group,
        "treatment_priority": patient.treatment_priority,
        "color": patient.color,
        "max_wait_minutes": patient.max_wait_minutes,
        "reevaluation_minutes": patient.reevaluation_minutes,
        "red_flags": patient.red_flags or [],
        "relevant_factors": patient.relevant_factors or [],
        "requires_human_review": patient.requires_human_review,
        "triage_result": patient.triage_result,
        "ai_severity": patient.ai_severity,
        "ai_reason": patient.ai_reason,
        "ai_explanation": patient.ai_explanation,
        "status": patient.status or STATUS_WAITING,
        "created_at": (
            patient.created_at.isoformat()
            if patient.created_at
            else None
        ),
        "updated_at": (
            patient.updated_at.isoformat()
            if patient.updated_at
            else None
        ),
    }


# --------------------------------------------------
# Create (called by the main /triage endpoint only)
# --------------------------------------------------

def save_assessment(
    patient_data: PatientData,
    triage_result: TriageResult,
    ai_assessment: AIAssessment,
    ai_explanation: str,
) -> dict:
    """
    Persists a full triage encounter and returns the stored row.
    """

    row = Patient(
        name=patient_data.name,
        age=patient_data.age,
        symptoms=[
            symptom.model_dump() for symptom in patient_data.symptoms
        ],
        vital_signs=patient_data.vital_signs.model_dump(),
        clinical_context=patient_data.clinical_context,
        triage_group=int(triage_result.suggested_group),
        treatment_priority=triage_result.treatment_priority,
        color=triage_result.color,
        max_wait_minutes=triage_result.max_wait_minutes,
        reevaluation_minutes=triage_result.reevaluation_minutes,
        red_flags=triage_result.red_flags,
        relevant_factors=triage_result.relevant_factors,
        requires_human_review=triage_result.requires_human_review,
        triage_result=triage_result.model_dump(mode="json"),
        ai_severity=ai_assessment.severity,
        ai_reason=ai_assessment.reason,
        ai_explanation=ai_explanation,
        status=STATUS_WAITING,
    )

    with _engine.begin() as connection:
        result = connection.execute(
            Patient.__table__.insert()
            .values(
                name=row.name,
                age=row.age,
                symptoms=row.symptoms,
                vital_signs=row.vital_signs,
                clinical_context=row.clinical_context,
                triage_group=row.triage_group,
                treatment_priority=row.treatment_priority,
                color=row.color,
                max_wait_minutes=row.max_wait_minutes,
                reevaluation_minutes=row.reevaluation_minutes,
                red_flags=row.red_flags,
                relevant_factors=row.relevant_factors,
                requires_human_review=row.requires_human_review,
                triage_result=row.triage_result,
                ai_severity=row.ai_severity,
                ai_reason=row.ai_reason,
                ai_explanation=row.ai_explanation,
                status=row.status,
                created_at=datetime.now(timezone.utc),
            )
            .returning(Patient.__table__)
        )
        stored = result.mappings().one()

    return dict(stored)


# Backwards-compatible alias.
def add_patient(patient_data: PatientData) -> int:
    with _engine.begin() as connection:
        result = connection.execute(
            Patient.__table__.insert()
            .values(
                name=patient_data.name,
                age=patient_data.age,
                symptoms=[
                    s.model_dump() for s in patient_data.symptoms
                ],
                vital_signs=patient_data.vital_signs.model_dump(),
                clinical_context=patient_data.clinical_context,
            )
            .returning(Patient.id)
        )
        return result.scalar_one()


# --------------------------------------------------
# Read
# --------------------------------------------------

def list_patients(include_done: bool = True) -> list[dict]:
    """
    Returns all patients ordered by urgency (most urgent first),
    then by how long they have been waiting (longest first).
    """

    statement = select(Patient)

    if not include_done:
        statement = statement.where(Patient.status != STATUS_DONE)

    # NULL triage groups sort last; lower group number = more urgent.
    statement = statement.order_by(
        func.coalesce(Patient.triage_group, 99).asc(),
        Patient.created_at.asc(),
    )

    with Session(_engine) as session:
        rows = session.scalars(statement).all()
        return [_serialize(row) for row in rows]


def get_patient(patient_id: int) -> dict | None:
    with Session(_engine) as session:
        row = session.scalars(
            select(Patient).where(Patient.id == patient_id)
        ).one_or_none()

        return _serialize(row) if row else None


# --------------------------------------------------
# Update
# --------------------------------------------------

_EDITABLE_FIELDS = {
    "name",
    "age",
    "symptoms",
    "vital_signs",
    "clinical_context",
}


def update_patient(patient_id: int, changes: dict) -> dict | None:
    values = {
        key: value
        for key, value in changes.items()
        if key in _EDITABLE_FIELDS
    }

    if values:
        with _engine.begin() as connection:
            connection.execute(
                update(Patient)
                .where(Patient.id == patient_id)
                .values(**values)
            )

    return get_patient(patient_id)


def set_status(patient_id: int, status: str) -> dict | None:
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    with _engine.begin() as connection:
        connection.execute(
            update(Patient)
            .where(Patient.id == patient_id)
            .values(status=status)
        )

    return get_patient(patient_id)


# --------------------------------------------------
# Delete
# --------------------------------------------------

def delete_patient(patient_id: int) -> bool:
    with _engine.begin() as connection:
        result = connection.execute(
            delete(Patient).where(Patient.id == patient_id)
        )

    return result.rowcount > 0


# --------------------------------------------------
# Statistics (dashboard)
# --------------------------------------------------

def get_stats() -> dict:
    """Aggregate counts for the analytics view."""

    with _engine.connect() as connection:
        total = connection.execute(
            select(func.count()).select_from(Patient)
        ).scalar_one()

        waiting = connection.execute(
            select(func.count())
            .select_from(Patient)
            .where(Patient.status == STATUS_WAITING)
        ).scalar_one()

        in_treatment = connection.execute(
            select(func.count())
            .select_from(Patient)
            .where(Patient.status == STATUS_IN_TREATMENT)
        ).scalar_one()

        done = connection.execute(
            select(func.count())
            .select_from(Patient)
            .where(Patient.status == STATUS_DONE)
        ).scalar_one()

        by_group_rows = connection.execute(
            select(Patient.triage_group, func.count())
            .group_by(Patient.triage_group)
        ).all()

    by_group = {str(group): count for group, count in by_group_rows}

    return {
        "total": total,
        "waiting": waiting,
        "in_treatment": in_treatment,
        "done": done,
        "by_group": by_group,
    }
