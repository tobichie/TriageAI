from app.models.patient import (
    PatientData,
    Symptom,
    VitalSigns
)

from app.triage.engine import (
    evaluate_patient
)


patient = PatientData(

    age=32,

    symptoms=[

        Symptom(

            name="heart attack",

            severity=5,

            duration_minutes=20

        )

    ],

    vital_signs=VitalSigns(

        heart_rate=105,

        oxygen_saturation=95,

        systolic_bp=120,

        diastolic_bp=80

    )

)


result = evaluate_patient(
    patient
)


print()

print(
    "TRIAGE GROUP:"
)

print(
    result.triage_group
)


print()

print(
    "FINDINGS:"
)


for finding in result.findings:

    print(
        finding
    )