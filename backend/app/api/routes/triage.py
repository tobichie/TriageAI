from fastapi import APIRouter


from app.models.patient import (
    PatientData
)


from app.models.triage_response import (
    AIAssessment,
    TriageResponse
)


from app.triage.engine import (
    evaluate_patient
)


from app.explainability.service import (

    generate_ai_assessment,

    generate_explanation

)


router = APIRouter()


@router.post(

    "/triage",

    response_model=TriageResponse

)

def triage_patient(

    patient: PatientData

) -> TriageResponse:


    # -------------------------
    # Deterministic triage
    # -------------------------

    triage_result = (

        evaluate_patient(
            patient
        )

    )


    # -------------------------
    # Independent AI assessment
    # -------------------------

    ai_assessment_data = (

        generate_ai_assessment(
            patient
        )

    )


    ai_assessment = (

        AIAssessment(

            severity=(
                ai_assessment_data[
                    "severity"
                ]
            ),

            reason=(
                ai_assessment_data[
                    "reason"
                ]
            )

        )

    )


    # -------------------------
    # AI explanation
    # -------------------------

    ai_explanation = (

        generate_explanation(

            patient,

            triage_result

        )

    )


    # -------------------------
    # Combined response
    # -------------------------

    return TriageResponse(

        triage_result=(
            triage_result
        ),

        ai_assessment=(
            ai_assessment
        ),

        ai_explanation=(
            ai_explanation
        )

    )