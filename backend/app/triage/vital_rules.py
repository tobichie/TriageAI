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


    evaluate_blood_pressure(
        vitals,
        findings
    )
    return findings

def evaluate_blood_pressure(

    vitals,

    findings: list[RuleFinding]

) -> None:

    if vitals.systolic_bp is None:

        return


    systolic_bp = (
        vitals.systolic_bp
    )


    thresholds = (
        VITAL_SIGN_THRESHOLDS[
            "blood_pressure"
        ]
    )


    # -------------------------
    # CRITICAL LOW
    # -------------------------

    if systolic_bp <= (
        thresholds[
            "critical_systolic_low_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_BP_CRITICAL_LOW"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Critically low systolic "
                    "blood pressure detected."
                ),

                observed_value=(
                    systolic_bp
                ),

                threshold=(
                    thresholds[
                        "critical_systolic_low_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )

        return


    # -------------------------
    # CRITICAL HIGH
    # -------------------------

    if systolic_bp >= (
        thresholds[
            "critical_systolic_high_min"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_BP_CRITICAL_HIGH"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Critically elevated systolic "
                    "blood pressure detected."
                ),

                observed_value=(
                    systolic_bp
                ),

                threshold=(
                    thresholds[
                        "critical_systolic_high_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )

        return


    # -------------------------
    # VERY URGENT LOW
    # -------------------------

    if systolic_bp <= (
        thresholds[
            "very_urgent_systolic_low_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_BP_VERY_URGENT_LOW"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Markedly low systolic "
                    "blood pressure detected."
                ),

                observed_value=(
                    systolic_bp
                ),

                threshold=(
                    thresholds[
                        "very_urgent_systolic_low_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.VERY_URGENT
                )
            )
        )

        return


    # -------------------------
    # VERY URGENT HIGH
    # -------------------------

    if systolic_bp >= (
        thresholds[
            "very_urgent_systolic_high_min"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_BP_VERY_URGENT_HIGH"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Markedly elevated systolic "
                    "blood pressure detected."
                ),

                observed_value=(
                    systolic_bp
                ),

                threshold=(
                    thresholds[
                        "very_urgent_systolic_high_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.VERY_URGENT
                )
            )
        )

        return


    # -------------------------
    # URGENT LOW
    # -------------------------

    if systolic_bp <= (
        thresholds[
            "urgent_systolic_low_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_BP_URGENT_LOW"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Low systolic blood pressure "
                    "detected."
                ),

                observed_value=(
                    systolic_bp
                ),

                threshold=(
                    thresholds[
                        "urgent_systolic_low_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )

        return


    # -------------------------
    # URGENT HIGH
    # -------------------------

    if systolic_bp >= (
        thresholds[
            "urgent_systolic_high_min"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_BP_URGENT_HIGH"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Elevated systolic blood "
                    "pressure detected."
                ),

                observed_value=(
                    systolic_bp
                ),

                threshold=(
                    thresholds[
                        "urgent_systolic_high_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )

def evaluate_oxygen_saturation(

    vitals,

    findings: list[RuleFinding]

) -> None:

    if vitals.oxygen_saturation is None:

        return


    oxygen_saturation = (
        vitals.oxygen_saturation
    )


    thresholds = (
        VITAL_SIGN_THRESHOLDS[
            "oxygen_saturation"
        ]
    )


    if oxygen_saturation <= (
        thresholds[
            "critical_max"
        ]
    ):

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
                    oxygen_saturation
                ),

                threshold=(
                    thresholds[
                        "critical_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )

        return


    if oxygen_saturation <= (
        thresholds[
            "very_urgent_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_SPO2_VERY_URGENT"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Markedly reduced oxygen "
                    "saturation detected."
                ),

                observed_value=(
                    oxygen_saturation
                ),

                threshold=(
                    thresholds[
                        "very_urgent_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.VERY_URGENT
                )
            )
        )

        return


    if oxygen_saturation <= (
        thresholds[
            "urgent_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_SPO2_URGENT"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Reduced oxygen saturation "
                    "detected."
                ),

                observed_value=(
                    oxygen_saturation
                ),

                threshold=(
                    thresholds[
                        "urgent_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )


def evaluate_heart_rate(

    vitals,

    findings: list[RuleFinding]

) -> None:

    if vitals.heart_rate is None:

        return


    heart_rate = (
        vitals.heart_rate
    )


    thresholds = (
        VITAL_SIGN_THRESHOLDS[
            "heart_rate"
        ]
    )


    # -------------------------
    # CRITICAL HIGH
    # -------------------------

    if heart_rate >= (
        thresholds[
            "critical_high_min"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_CRITICAL_HIGH"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Critically elevated "
                    "heart rate detected."
                ),

                observed_value=(
                    heart_rate
                ),

                threshold=(
                    thresholds[
                        "critical_high_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )

        return


    # -------------------------
    # CRITICAL LOW
    # -------------------------

    if heart_rate <= (
        thresholds[
            "critical_low_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_CRITICAL_LOW"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Critically reduced "
                    "heart rate detected."
                ),

                observed_value=(
                    heart_rate
                ),

                threshold=(
                    thresholds[
                        "critical_low_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.IMMEDIATE
                )
            )
        )

        return


    # -------------------------
    # VERY URGENT HIGH
    # -------------------------

    if heart_rate >= (
        thresholds[
            "very_urgent_high_min"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_VERY_URGENT_HIGH"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Markedly elevated "
                    "heart rate detected."
                ),

                observed_value=(
                    heart_rate
                ),

                threshold=(
                    thresholds[
                        "very_urgent_high_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.VERY_URGENT
                )
            )
        )

        return


    # -------------------------
    # VERY URGENT LOW
    # -------------------------

    if heart_rate <= (
        thresholds[
            "very_urgent_low_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_VERY_URGENT_LOW"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Markedly reduced "
                    "heart rate detected."
                ),

                observed_value=(
                    heart_rate
                ),

                threshold=(
                    thresholds[
                        "very_urgent_low_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.VERY_URGENT
                )
            )
        )

        return


    # -------------------------
    # URGENT HIGH
    # -------------------------

    if heart_rate >= (
        thresholds[
            "urgent_high_min"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_URGENT_HIGH"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Elevated heart rate detected."
                ),

                observed_value=(
                    heart_rate
                ),

                threshold=(
                    thresholds[
                        "urgent_high_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )

        return


    # -------------------------
    # URGENT LOW
    # -------------------------

    if heart_rate <= (
        thresholds[
            "urgent_low_max"
        ]
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    "VITAL_HEART_RATE_URGENT_LOW"
                ),

                category=(
                    RuleCategory.VITAL_SIGN
                ),

                description=(
                    "Reduced heart rate detected."
                ),

                observed_value=(
                    heart_rate
                ),

                threshold=(
                    thresholds[
                        "urgent_low_max"
                    ]
                ),

                comparison="<=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )