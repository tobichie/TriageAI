from pydantic import BaseModel

from app.safety.status import AssessmentStatus


class SafetyResult(BaseModel):

    assessment_status: AssessmentStatus

    warnings: list[str]

    requires_human_review: bool