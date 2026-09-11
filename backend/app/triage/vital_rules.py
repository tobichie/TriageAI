from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)

from app.protocols.prototype_v1 import (
    VITAL_SIGN_THRESHOLDS
)

from app.triage.priorities import (
    TriageGroup
)


def evaluate_vital_signs(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []

    vitals = patient.vital_signs


    evaluate_oxygen_saturation(
        vitals,
        findings
    )

    evaluate_heart_rate(
        vitals,
        findings
    )


    return findings


def evaluate_oxygen_saturation(
    vitals,
    findings: list[RuleFinding]
) -> None:

    if vitals.oxygen_saturation is None:

        return


    threshold = (
        VITAL_SIGN_THRESHOLDS[
            "oxygen_saturation"
        ][
            "critical_max"
        ]
    )


    if vitals.oxygen_saturation <= threshold:
        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_SPO2_CRITICAL"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Critically low oxygen "
                    "saturation detected."
                ),

                observed_value=(
                    vitals.oxygen_saturation
                ),

                threshold=(
                    threshold
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )


def evaluate_heart_rate(
    vitals,
    findings: list[RuleFinding]
) -> None:

    if vitals.heart_rate is None:

        return


    threshold = (
        VITAL_SIGN_THRESHOLDS[
            "heart_rate"
        ][
            "critical_min"
        ]
    )


    if vitals.heart_rate >= threshold:
        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_CRITICAL"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Critically abnormal "
                    "heart rate detected."
                ),

                observed_value=(
                    vitals.heart_rate
                ),

                threshold=(
                    threshold
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )