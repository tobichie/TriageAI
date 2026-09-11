from app.models.patient import PatientData

from app.models.triage_result import (
    RuleCategory,
    RuleFinding,
    TriageResult
)

from app.triage.missing_information import (
    detect_missing_information
)

from app.triage.priorities import (
    TriageGroup,
    TRIAGE_GROUPS
)

from app.triage.red_flags import (
    evaluate_red_flags
)

from app.triage.symptom_rules import (
    evaluate_symptoms
)

from app.triage.vital_rules import (
    evaluate_vital_signs
)


def get_most_urgent_group(
    findings: list[RuleFinding]
) -> TriageGroup:

    if not findings:

        return TriageGroup.NOT_URGENT


    return min(
        finding.suggested_group
        for finding in findings
    )


def evaluate_all_rules(
    patient: PatientData
) -> list[RuleFinding]:

    findings = []


    red_flag_findings = (
        evaluate_red_flags(patient)
    )

    vital_findings = (
        evaluate_vital_signs(patient)
    )

    symptom_findings = (
        evaluate_symptoms(patient)
    )


    findings.extend(red_flag_findings)

    findings.extend(vital_findings)

    findings.extend(symptom_findings)


    return findings


def evaluate_patient(
    patient: PatientData
) -> TriageResult:

    findings = evaluate_all_rules(
        patient
    )


    suggested_group = (
        get_most_urgent_group(
            findings
        )
    )


    group_info = TRIAGE_GROUPS[
        suggested_group
    ]


    missing_information = (
        detect_missing_information(
            patient
        )
    )


    triggered_rules = [

        finding.rule_id

        for finding in findings
    ]


    relevant_factors = [

        finding.description

        for finding in findings
    ]

    red_flags = [

        finding.description

        for finding in findings

        if finding.category == RuleCategory.RED_FLAG
    ]


    return TriageResult(

        suggested_group=suggested_group,

        treatment_priority=(
            group_info.treatment_priority
        ),

        color=group_info.color,

        max_wait_minutes=(
            group_info.max_wait_minutes
        ),

        reevaluation_minutes=(
            group_info.reevaluation_minutes
        ),

        triggered_rules=triggered_rules,

        red_flags=red_flags,

        relevant_factors=relevant_factors,

        missing_information=(
            missing_information
        ),

        requires_human_review=True
    )