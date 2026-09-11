from app.models.patient import (
    PatientData,
    VitalSigns
)

from app.triage.missing_information import (
    detect_missing_information
)


def test_detect_missing_information():

    patient = PatientData(

        age=None,

        symptoms=[],

        vital_signs=VitalSigns()
    )


    missing = detect_missing_information(
        patient
    )


    assert "age" in missing

    assert "symptoms" in missing

    assert "heart_rate" in missing

    assert "systolic_bp" in missing

    assert "diastolic_bp" in missing

    assert "oxygen_saturation" in missing