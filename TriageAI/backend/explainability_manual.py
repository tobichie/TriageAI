from app.models.patient import (
    PatientData,
    VitalSigns,
    Symptom
)

from app.triage.engine import evaluate_patient

from app.explainability.service import (
    generate_explanation,
    generate_ai_assessment
)


patient = PatientData(

    age=74,

    symptoms=[
        Symptom(
            name="heart attack",
            duration_minutes=80,
            severity=3
        )
    ],

    vital_signs=VitalSigns(

        heart_rate=120,

        systolic_bp=120,

        diastolic_bp=80,

        oxygen_saturation=86
    ),

    clinical_context=(
        "Prototype explainability test"
    )
)


triage_result = evaluate_patient(
    patient
)


explanation = generate_explanation(

    patient,

    triage_result
)

ai_assessment = generate_ai_assessment(patient)

print("\n--- TRIAGE RESULT ---\n")

print(triage_result)


print("\n--- AI EXPLANATION ---\n")

print(explanation)

print("\n--- AI ASSESSMENT ---\n")

print(ai_assessment)