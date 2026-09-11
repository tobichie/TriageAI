from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)

from app.protocols.symptom_rules_v1 import (
    CRITICAL_SYMPTOMS,
    VERY_URGENT_SYMPTOMS,
    URGENT_SYMPTOMS,
    SYMPTOM_RULES,
    SYMPTOM_ALIASES
)

from app.triage.normalization import (
    normalize_text
)

from app.triage.priorities import (
    TriageGroup
)

def resolve_symptom_name(
    symptom_name: str
) -> str:

    return (
        SYMPTOM_ALIASES.get(
            symptom_name,
            symptom_name
        )
    )

def evaluate_symptoms(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []


    for symptom in patient.symptoms:

        normalized_name = (
            normalize_text(
                symptom.name
            )
        )


        symptom_name = (
            resolve_symptom_name(
                normalized_name
            )
        )

        evaluate_critical_symptom(
            symptom_name,
            findings
        )

        evaluate_very_urgent_symptom(
            symptom_name,
            findings
        )

        evaluate_urgent_symptom(
            symptom_name,
            findings
        )

        evaluate_structured_symptom(
            symptom,
            symptom_name,
            findings
        )



    return findings

def evaluate_very_urgent_symptom(

    symptom_name: str,

    findings: list[RuleFinding]

) -> None:

    if (
        symptom_name
        not in VERY_URGENT_SYMPTOMS
    ):

        return


    findings.append(

        RuleFinding(

            rule_id=(
                VERY_URGENT_SYMPTOMS[
                    symptom_name
                ][
                    "rule_id"
                ]
            ),

            category=(
                RuleCategory.SYMPTOM
            ),

            description=(
                VERY_URGENT_SYMPTOMS[
                    symptom_name
                ][
                    "description"
                ]
            ),

            observed_value=(
                symptom_name
            ),

            suggested_group=(
                TriageGroup.VERY_URGENT
            )
        )
    )


def evaluate_structured_symptom(

    symptom,

    symptom_name: str,

    findings: list[RuleFinding]

) -> None:

    if (
        symptom_name
        not in SYMPTOM_RULES
    ):

        return


    rule = (
        SYMPTOM_RULES[
            symptom_name
        ]
    )


    evaluate_symptom_severity(

        symptom,

        symptom_name,

        rule,

        findings
    )


    evaluate_symptom_duration(

        symptom,

        symptom_name,

        rule,

        findings
    )

def evaluate_symptom_severity(

    symptom,

    symptom_name: str,

    rule: dict,

    findings: list[RuleFinding]

) -> None:

    if symptom.severity is None:

        return


    if "severity" not in rule:

        return


    severity_rules = (
        rule["severity"]
    )


    severity = (
        symptom.severity
    )


    if (
        "very_urgent_min"
        in severity_rules

        and severity >= (
            severity_rules[
                "very_urgent_min"
            ]
        )
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    f"SYMPTOM_{symptom_name.upper()}_VERY_URGENT"
                ),

                category=(
                    RuleCategory.SYMPTOM
                ),

                description=(
                    f"Very severe "
                    f"{symptom_name.replace('_', ' ')} "
                    f"reported."
                ),

                observed_value=(
                    severity
                ),

                threshold=(
                    severity_rules[
                        "very_urgent_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.VERY_URGENT
                )
            )
        )

        return


    if (
        "urgent_min"
        in severity_rules

        and severity >= (
            severity_rules[
                "urgent_min"
            ]
        )
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    f"SYMPTOM_{symptom_name.upper()}_URGENT"
                ),

                category=(
                    RuleCategory.SYMPTOM
                ),

                description=(
                    f"Severe "
                    f"{symptom_name.replace('_', ' ')} "
                    f"reported."
                ),

                observed_value=(
                    severity
                ),

                threshold=(
                    severity_rules[
                        "urgent_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )

        return


    if (
        "normal_min"
        in severity_rules

        and severity >= (
            severity_rules[
                "normal_min"
            ]
        )
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    f"SYMPTOM_{symptom_name.upper()}_NORMAL"
                ),

                category=(
                    RuleCategory.SYMPTOM
                ),

                description=(
                    f"Moderate "
                    f"{symptom_name.replace('_', ' ')} "
                    f"reported."
                ),

                observed_value=(
                    severity
                ),

                threshold=(
                    severity_rules[
                        "normal_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.NORMAL
                )
            )
        )

        return


    if (
        "not_urgent_min"
        in severity_rules

        and severity >= (
            severity_rules[
                "not_urgent_min"
            ]
        )
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    f"SYMPTOM_{symptom_name.upper()}_NOT_URGENT"
                ),

                category=(
                    RuleCategory.SYMPTOM
                ),

                description=(
                    f"Mild "
                    f"{symptom_name.replace('_', ' ')} "
                    f"reported."
                ),

                observed_value=(
                    severity
                ),

                threshold=(
                    severity_rules[
                        "not_urgent_min"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.NOT_URGENT
                )
            )
        )

def evaluate_symptom_duration(

    symptom,

    symptom_name: str,

    rule: dict,

    findings: list[RuleFinding]

) -> None:

    if symptom.duration_minutes is None:

        return


    if "duration" not in rule:

        return


    duration_rules = (
        rule["duration"]
    )


    duration = (
        symptom.duration_minutes
    )


    if (
        "urgent_min_minutes"
        in duration_rules

        and duration >= (
            duration_rules[
                "urgent_min_minutes"
            ]
        )
    ):

        findings.append(

            RuleFinding(

                rule_id=(
                    f"SYMPTOM_{symptom_name.upper()}_PROLONGED"
                ),

                category=(
                    RuleCategory.SYMPTOM
                ),

                description=(
                    f"Prolonged "
                    f"{symptom_name.replace('_', ' ')} "
                    f"reported."
                ),

                observed_value=(
                    duration
                ),

                threshold=(
                    duration_rules[
                        "urgent_min_minutes"
                    ]
                ),

                comparison=">=",

                suggested_group=(
                    TriageGroup.URGENT
                )
            )
        )

def evaluate_critical_symptom(

    symptom_name: str,

    findings: list[RuleFinding]

) -> None:


    if (
        symptom_name
        not in CRITICAL_SYMPTOMS
    ):

        return


    findings.append(

        RuleFinding(

            rule_id=(
                CRITICAL_SYMPTOMS[
                    symptom_name
                ][
                    "rule_id"
                ]
            ),

            category=(
                RuleCategory.SYMPTOM
            ),

            description=(
                CRITICAL_SYMPTOMS[
                    symptom_name
                ][
                    "description"
                ]
            ),

            observed_value=(
                symptom_name
            ),

            suggested_group=(
                TriageGroup.IMMEDIATE
            )
        )
    )


def evaluate_urgent_symptom(

    symptom_name: str,

    findings: list[RuleFinding]

) -> None:


    if (
        symptom_name
        not in URGENT_SYMPTOMS
    ):

        return


    findings.append(

        RuleFinding(

            rule_id=(
                URGENT_SYMPTOMS[
                    symptom_name
                ][
                    "rule_id"
                ]
            ),

            category=(
                RuleCategory.SYMPTOM
            ),

            description=(
                URGENT_SYMPTOMS[
                    symptom_name
                ][
                    "description"
                ]
            ),

            observed_value=(
                symptom_name
            ),

            suggested_group=(
                TriageGroup.URGENT
            )
        )
    )