"""
Privacy guardrail: the patient's identifying name must never be sent to
the external AI (OpenAI). These tests assert that the two prompt-context
builders exclude the ``name`` field and that a distinctive name value
does not appear anywhere in the serialized payload.

If someone later wires ``patient.name`` into an AI context, these tests
fail loudly instead of silently leaking PII.
"""

import json

from app.models.patient import PatientData, Symptom, VitalSigns
from app.triage.engine import evaluate_patient
from app.explainability.service import (
    build_ai_assessment_context,
    build_explanation_context,
)


SECRET_NAME = "Zzyzx Uniquename-Testperson"


def _patient() -> PatientData:
    return PatientData(
        name=SECRET_NAME,
        age=67,
        symptoms=[
            Symptom(name="chest pain", severity=8, duration_minutes=20)
        ],
        vital_signs=VitalSigns(
            heart_rate=128,
            systolic_bp=95,
            diastolic_bp=60,
            oxygen_saturation=93,
        ),
        clinical_context="History of hypertension",
    )


def test_ai_assessment_context_excludes_name():
    context = build_ai_assessment_context(_patient())

    assert "name" not in context
    assert SECRET_NAME not in json.dumps(context, default=str)


def test_explanation_context_excludes_name():
    patient = _patient()
    triage_result = evaluate_patient(patient)

    context = build_explanation_context(patient, triage_result)

    assert "name" not in context["patient_data"]
    assert SECRET_NAME not in json.dumps(context, default=str)


def test_symptom_name_is_still_present():
    # Guard against an over-eager filter that strips symptom names too.
    context = build_ai_assessment_context(_patient())

    assert context["symptoms"][0]["name"] == "chest pain"
