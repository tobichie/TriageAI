import json
import os

from dotenv import load_dotenv

from openai import OpenAI

from app.explainability.prompts import (
    SYSTEM_PROMPT,
    MODEL_PROMPT,
    MODEL_NAME
)

from app.models.patient import (
    PatientData
)

from app.models.triage_result import (
    TriageResult
)


load_dotenv()


api_key = os.getenv(
    "OPENAI_API_KEY"
)

VECTOR_STORE_ID = os.getenv(
    "VECTOR_STORE_ID"
)

if not api_key:

    raise RuntimeError(
        "OPENAI_API_KEY is not configured."
    )


client = OpenAI(
    api_key=api_key
)

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
        5
    }:

        raise ValueError(
            "'severity' must be "
            "between 1 and 5."
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

            "symptoms": patient.symptoms,

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


    context = (
        build_explanation_context(

            patient,

            triage_result
        )
    )


    response = client.responses.create(

        model=MODEL_NAME,

        instructions=SYSTEM_PROMPT,

        input=json.dumps(

            context,

            indent=2,

            default=str
        )
    )

    return response.output_text

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

    context = (
        build_ai_assessment_context(
            patient
        )
    )

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=MODEL_PROMPT,
        input=json.dumps(context),

        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
            }
        ],
    )


    result = (
        response.output_text
        .strip()
    )


    return validate_ai_assessment(
        result
    )