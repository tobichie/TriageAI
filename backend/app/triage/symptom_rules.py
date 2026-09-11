from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)


def evaluate_symptoms(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []


    for symptom in patient.symptoms:

        symptom_name = (
            symptom.name
            .strip()
            .lower()
        )


        # Prototype symptom rules
        # will be added here.


    return findings