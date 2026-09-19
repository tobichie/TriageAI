from app.models.patient import (
    PatientData,
    VitalSigns, Symptom
)

from app.triage.vital_rules import (
    evaluate_vital_signs
)


def test_vitals(
    oxygen_saturation,
    heart_rate,
    systolic_bp,
    diastolic_bp
):

    patient = PatientData(

        age=30,
        symptoms=[

            Symptom(
                name="chest pain",
                severity=8,
                duration_minutes=30
            ),

            Symptom(
                name="shortness of breath",
                severity=7,
                duration_minutes=15
            )

        ],

        vital_signs=VitalSigns(

            oxygen_saturation=(
                oxygen_saturation
            ),

            heart_rate=(
                heart_rate
            ),

            systolic_bp=(
                systolic_bp
            ),

            diastolic_bp=(
                diastolic_bp
            )

        ),

        clinical_context=(
            "Manual vital sign test"
        )

    )


    findings = (
        evaluate_vital_signs(
            patient
        )
    )


    print()

    print(
        "--- VITAL SIGN TEST ---"
    )

    print()

    print(
        f"SpO2: "
        f"{oxygen_saturation}"
    )

    print(
        f"Heart rate: "
        f"{heart_rate}"
    )

    print(
        f"Blood pressure: "
        f"{systolic_bp}/{diastolic_bp}"
    )

    print()

    if not findings:

        print(
            "No findings."
        )


    for finding in findings:

        print(
            finding
        )


# -------------------------
# TEST CASE
# -------------------------

test_vitals(

    oxygen_saturation=86,

    heart_rate=120,

    systolic_bp=85,

    diastolic_bp=60

)