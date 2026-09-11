from app.models.patient import (
    PatientData,
    Symptom,
    VitalSigns
)

from app.triage.vital_rules import (
    evaluate_vital_signs
)

from app.triage.priorities import (
    TriageGroup
)


def test_critical_oxygen_saturation():

    patient = PatientData(

        age=30,

        symptoms=[

            Symptom(
                name="headache"
            )
        ],

        vital_signs=VitalSigns(

            heart_rate=80,

            systolic_bp=120,

            diastolic_bp=80,

            oxygen_saturation=32
        )
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert len(findings) == 1

    assert findings[0].rule_id == (
        "VITAL_SPO2_CRITICAL"
    )

    assert findings[0].suggested_group == (
        TriageGroup.IMMEDIATE
    )
def test_critical_heart_rate():

    patient = PatientData(

        age=30,

        symptoms=[

            Symptom(
                name="headache"
            )
        ],

        vital_signs=VitalSigns(

            heart_rate=170,

            systolic_bp=120,

            diastolic_bp=80,

            oxygen_saturation=98
        )
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert len(findings) == 1

    assert findings[0].rule_id == (
        "VITAL_HEART_RATE_CRITICAL"
    )

    assert findings[0].suggested_group == (
        TriageGroup.IMMEDIATE
    )

def test_multiple_critical_vital_signs():

    patient = PatientData(

        age=30,

        symptoms=[

            Symptom(
                name="headache"
            )
        ],

        vital_signs=VitalSigns(

            heart_rate=170,

            systolic_bp=120,

            diastolic_bp=80,

            oxygen_saturation=32
        )
    )


    findings = evaluate_vital_signs(
        patient
    )


    rule_ids = [

        finding.rule_id

        for finding in findings
    ]


    assert "VITAL_SPO2_CRITICAL" in rule_ids

    assert (
        "VITAL_HEART_RATE_CRITICAL"
        in rule_ids
    )