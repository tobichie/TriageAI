from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)

from app.protocols.symptom_rules_v1 import (
    CRITICAL_SYMPTOMS,
    URGENT_SYMPTOMS
)

from app.triage.normalization import (
    normalize_text
)

from app.triage.priorities import (
    TriageGroup
)


def evaluate_symptoms(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []


    for symptom in patient.symptoms:

        symptom_name = normalize_text(
            symptom.name
        )


        evaluate_critical_symptom(
            symptom_name,
            findings
        )


        evaluate_urgent_symptom(
            symptom_name,
            findings
        )


    return findings


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