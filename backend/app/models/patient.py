from typing import Optional

from pydantic import BaseModel, Field


class VitalSigns(BaseModel):

    heart_rate: Optional[int] = Field(
        default=None,
        ge=0,
        le=300
    )

    systolic_bp: Optional[int] = Field(
        default=None,
        ge=0,
        le=300
    )

    diastolic_bp: Optional[int] = Field(
        default=None,
        ge=0,
        le=200
    )

    oxygen_saturation: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )


class Symptom(BaseModel):

    name: str

    severity: Optional[int] = None

    duration_minutes: Optional[int] = Field(
        default=None,
        ge=0
    )


class PatientData(BaseModel):

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=130
    )

    symptoms: list[Symptom] = Field(
        default_factory=list
    )

    vital_signs: VitalSigns

    clinical_context: Optional[str] = None