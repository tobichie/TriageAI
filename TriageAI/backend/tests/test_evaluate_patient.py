from app.models.patient import (
    PatientData,
    VitalSigns
)

from app.triage.engine import (
    evaluate_patient
)

from app.triage.priorities import (
    TriageGroup
)


def test_evaluate_patient_returns_result():

    patient = PatientData(

        age=30,

        symptoms=[],

        vital_signs=VitalSigns(
            heart_rate=80,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98
        )
    )


    result = evaluate_patient(
        patient
    )


    assert result.suggested_group == (
        TriageGroup.NOT_URGENT
    )


    assert result.treatment_priority == (
        "Nicht dringend" # for future: We should not blindly treat “no triggered rule” as clinically equivalent to “not urgent.”
    )


    assert result.color == "blue"


    assert result.max_wait_minutes == 120


    assert result.reevaluation_minutes == 120


    assert result.requires_human_review is True