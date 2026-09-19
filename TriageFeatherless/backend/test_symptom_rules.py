from app.models.patient import (
    PatientData,
    Symptom,
    VitalSigns
)

from app.triage.symptom_rules import (
    evaluate_symptoms
)
from app.triage.priorities import (
    TriageGroup
)


def test_unconsciousness_is_immediate():

    patient = PatientData(

        age=50,

        symptoms=[

            Symptom(

                name=(
                    "loss of consciousness"
                ),

                severity=10,

                duration_minutes=5
            )

        ],

        vital_signs=VitalSigns(),

        clinical_context="Test"
    )


    findings = (
        evaluate_symptoms(
            patient
        )
    )


    assert any(

        finding.suggested_group
        == TriageGroup.IMMEDIATE

        for finding in findings
    )

def test_severe_chest_pain():

    patient = PatientData(

        age=50,

        symptoms=[

            Symptom(

                name="chest pain",

                severity=9,

                duration_minutes=60
            )

        ],

        vital_signs=VitalSigns(),

        clinical_context="Test"
    )


    findings = (
        evaluate_symptoms(
            patient
        )
    )


    assert len(findings) >= 1


    assert any(

        finding.rule_id
        == (
            "SYMPTOM_CHEST_PAIN_VERY_URGENT"
        )

        for finding in findings
    )