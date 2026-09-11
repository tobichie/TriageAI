from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding
)

from app.triage.priorities import (
    TriageGroup
)


def evaluate_red_flags(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []

    for symptom in patient.symptoms:

        symptom_name = (
            symptom.name
            .strip()
            .lower()
        )

        severity = (
            symptom.severity
            .strip()
            .lower()
            if symptom.severity
            else None
        )


        if (
            symptom_name == "example_critical_symptom"
        ):

            findings.append(

                RuleFinding(

                    rule_id="RED_FLAG_001",

                    category=RuleCategory.RED_FLAG,

                    description=(
                        "Prototype critical symptom "
                        "identified."
                    ),

                    suggested_group=(
                        TriageGroup.IMMEDIATE
                    )
                )
            )


    return findings