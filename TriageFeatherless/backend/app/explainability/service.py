import json
import os

import requests

from dotenv import load_dotenv

from app.explainability.prompts import (
    SYSTEM_PROMPT,
    MODEL_PROMPT,
)

from app.models.patient import (
    PatientData
)

from app.models.triage_result import (
    TriageResult
)


load_dotenv()


FEATHERLESS_KEY = os.getenv(
    "FEATHERLESS_KEY"
)

MODEL_NAME = (
    "EpistemeAI/Reasoning-Medical0.1-27B"
)

FEATHERLESS_URL = (
    "https://api.featherless.ai/v1/chat/completions"
)


if not FEATHERLESS_KEY:

    raise RuntimeError(
        "FEATHERLESS_KEY is not configured."
    )


def featherless_request(
    messages: list
) -> str:

    response = requests.post(

        FEATHERLESS_URL,

        headers={

            "Authorization": (
                f"Bearer {FEATHERLESS_KEY}"
            ),

            "Content-Type": (
                "application/json"
            ),

            "HTTP-Referer": (
                "ichmagfunnyfrisch.chips"
            ),

            "X-Title": "TriageAI"

        },

        json={

            "model": MODEL_NAME,

            "messages": messages,

            "temperature": 0,

            "max_tokens": 2048

        },

        timeout=120

    )


    if not response.ok:

        raise RuntimeError(

            "Featherless API request failed: "

            f"{response.status_code} "

            f"{response.text}"

        )


    try:

        data = response.json()

    except ValueError as error:

        raise RuntimeError(

            "Featherless returned invalid JSON: "

            f"{response.text}"

        ) from error


    try:

        content = (
            data["choices"][0]
            ["message"]["content"]
        )

    except (
        KeyError,
        IndexError,
        TypeError
    ) as error:

        raise RuntimeError(

            "Unexpected Featherless response: "
            f"{data}"

        ) from error


    if not isinstance(
        content,
        str
    ):

        raise RuntimeError(
            "Featherless returned no text content."
        )


    return content


def validate_ai_assessment(
    result: str
) -> dict:

    try:

        assessment = json.loads(
            result
        )

    except json.JSONDecodeError as error:

        raise ValueError(

            "Invalid AI assessment JSON: "
            f"{result}"

        ) from error


    if not isinstance(
        assessment,
        dict
    ):

        raise ValueError(
            "AI assessment must be "
            "a JSON object."
        )


    if "severity" not in assessment:

        raise ValueError(
            "AI assessment is missing "
            "'severity'."
        )


    if "reason" not in assessment:

        raise ValueError(
            "AI assessment is missing "
            "'reason'."
        )


    severity = assessment[
        "severity"
    ]

    reason = assessment[
        "reason"
    ]


    if (
        not isinstance(
            severity,
            int
        )

        or isinstance(
            severity,
            bool
        )
    ):

        raise ValueError(
            "'severity' must be an integer."
        )


    if severity not in {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10
    }:

        raise ValueError(
            "'severity' must be "
            "between 1 and 10."
        )


    if (
        not isinstance(
            reason,
            str
        )

        or not reason.strip()
    ):

        raise ValueError(
            "'reason' must be "
            "a non-empty string."
        )


    return {

        "severity": severity,

        "reason": reason.strip()

    }


def build_explanation_context(

    patient: PatientData,

    triage_result: TriageResult

) -> dict:

    return {

        "patient_data": {

            "age": patient.age,

            "symptoms": [

                symptom.model_dump(
                    mode="json"
                )

                for symptom in patient.symptoms

            ],

            "vital_signs": (
                patient.vital_signs.model_dump()
            ),

            "clinical_context": (
                patient.clinical_context
            )

        },


        "deterministic_engine_result": {

            "protocol_name": (
                triage_result.protocol_name
            ),

            "protocol_version": (
                triage_result.protocol_version
            ),

            "suggested_group": (
                triage_result.suggested_group
            ),

            "treatment_priority": (
                triage_result.treatment_priority
            ),

            "color": (
                triage_result.color
            ),

            "max_wait_minutes": (
                triage_result.max_wait_minutes
            ),

            "reevaluation_minutes": (
                triage_result.reevaluation_minutes
            ),

            "rule_findings": [

                finding.model_dump(
                    mode="json"
                )

                for finding in (
                    triage_result.rule_findings
                )

            ],

            "triggered_rules": (
                triage_result.triggered_rules
            ),

            "red_flags": (
                triage_result.red_flags
            ),

            "relevant_factors": (
                triage_result.relevant_factors
            )

        },


        "safety_information": {

            "missing_information": (
                triage_result.missing_information
            ),

            "assessment_status": (
                triage_result.assessment_status
            ),

            "safety_warnings": (
                triage_result.safety_warnings
            ),

            "requires_human_review": (
                triage_result.requires_human_review
            )

        }

    }


def generate_explanation(

    patient: PatientData,

    triage_result: TriageResult

) -> str:

    context = build_explanation_context(
        patient,
        triage_result
    )


    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": json.dumps(
                context,
                indent=2,
                default=str
            )
        }

    ]


    return featherless_request(
        messages
    )


def build_ai_assessment_context(

    patient: PatientData

) -> dict:

    return {

        "age": patient.age,

        "symptoms": [

            {

                "name": symptom.name,

                "severity": (
                    symptom.severity
                ),

                "duration_minutes": (
                    symptom.duration_minutes
                )

            }

            for symptom in patient.symptoms

        ],

        "vital_signs": (
            patient.vital_signs.model_dump()
        ),

        "clinical_context": (
            patient.clinical_context
        )

    }


def generate_ai_assessment(

    patient: PatientData

) -> dict:

    context = build_ai_assessment_context(
        patient
    )


    messages = [

        {
            "role": "system",
            "content": MODEL_PROMPT
        },

        {
            "role": "user",
            "content": json.dumps(
                context,
                indent=2,
                default=str
            )
        }

    ]


    result = featherless_request(
        messages
    )


    result = result.strip()


    return validate_ai_assessment(
        result
    )
