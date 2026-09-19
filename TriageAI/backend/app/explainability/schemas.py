from pydantic import BaseModel


class ExplanationResult(BaseModel):

    summary: str

    explanation: str

    important_factors: list[str]

    missing_information: list[str]

    safety_note: str