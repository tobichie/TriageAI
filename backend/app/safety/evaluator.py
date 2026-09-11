from app.safety.result import SafetyResult

from app.safety.status import AssessmentStatus


def evaluate_safety(
    missing_information: list[str]
) -> SafetyResult:

    warnings = []

    if missing_information:

        warnings.append(
            "Assessment contains missing information."
        )

        for item in missing_information:

            warnings.append(
                f"Missing information: {item}"
            )

        return SafetyResult(

            assessment_status=AssessmentStatus.INCOMPLETE,

            warnings=warnings,

            requires_human_review=True
        )


    warnings.append(
        "Assessment requires human review."
    )


    return SafetyResult(

        assessment_status=AssessmentStatus.REQUIRES_REVIEW,

        warnings=warnings,

        requires_human_review=True
    )