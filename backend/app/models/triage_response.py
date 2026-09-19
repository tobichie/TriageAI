from pydantic import BaseModel


from app.models.triage_result import (
    TriageResult
)


class AIAssessment(
    BaseModel):


    severity: int


    reason: str


class TriageResponse(
    BaseModel):


    patient_id: int | None = None


    triage_result: TriageResult


    ai_assessment: (
        AIAssessment
    )


    ai_explanation: str