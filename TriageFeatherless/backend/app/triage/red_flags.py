from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)

from app.triage.normalization import (
    normalize_text
)

from app.triage.priorities import (
    TriageGroup
)


def evaluate_red_flags(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []


    for symptom in patient.symptoms:

        symptom_name = normalize_text(
            symptom.name
        )


        severity = (
            symptom.severity
        )


        if (
            symptom_name
            == "example_critical_symptom"
        ):

            findings.append(

                RuleFinding(

                    rule_id=(
                        "RED_FLAG_001"
                    ),

                    category=(
                        RuleCategory.RED_FLAG
                    ),

                    description=(
                        "Prototype critical "
                        "symptom identified."
                    ),

                    observed_value=(
                        symptom_name
                    ),

                    suggested_group=(
                        TriageGroup.IMMEDIATE
                    )
                )
            )


    return findings