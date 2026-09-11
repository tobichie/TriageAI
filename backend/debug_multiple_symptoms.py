from app.models.patient import (
    PatientData,
    Symptom,
    VitalSigns
)

from app.triage.symptom_rules import (
    extract_symptom_names,
    evaluate_symptoms
)


combined_symptom = (
    "chest pain shortness of breath"
)


print("\nExtraction test:")
print(
    extract_symptom_names(
        combined_symptom
    )
)


patient = PatientData(

    age=32,

    symptoms=[

        Symptom(
            name=(
                "chest pain shortness of breath"
            ),
            severity=3,
            duration_minutes=20
        ),

        Symptom(
            name="headache",
            severity=2,
            duration_minutes=10
        )

    ],

    vital_signs=VitalSigns(
        heart_rate=80,
        systolic_bp=120,
        diastolic_bp=80,
        oxygen_saturation=97
    )

)


findings = evaluate_symptoms(
    patient
)


print("\nFindings:")

for finding in findings:

    print(
        finding.rule_id,
        "|",
        finding.suggested_group,
        "|",
        finding.description
    )