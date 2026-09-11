from fastapi import APIRouter

from app.models.patient import PatientData
from app.models.triage_result import TriageResult

from app.triage.engine import evaluate_patient


router = APIRouter()


@router.post(
    "/triage",
    response_model=TriageResult
)
def triage_patient(
    patient: PatientData
) -> TriageResult:

    result = evaluate_patient(
        patient
    )

    return result