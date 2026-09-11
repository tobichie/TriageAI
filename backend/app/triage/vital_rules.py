from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)


def evaluate_vital_signs(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []

    vitals = patient.vital_signs


    # Prototype placeholder.
    #
    # Clinical thresholds should be added
    # from an approved triage protocol.


    return findings