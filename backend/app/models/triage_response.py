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


    triage_result: TriageResult


    ai_assessment: (
        AIAssessment
    )


    ai_explanation: str