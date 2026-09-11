from enum import Enum
from typing import Any
from pydantic import BaseModel

from app.triage.priorities import TriageGroup
from app.safety.status import AssessmentStatus


class RuleCategory(str, Enum):

    RED_FLAG = "red_flag"
    VITAL_SIGN = "vital_sign"
    SYMPTOM = "symptom"


class RuleFinding(BaseModel):

    rule_id: str

    category: RuleCategory

    description: str

    suggested_group: TriageGroup


    observed_value: Any | None = None

    threshold: Any | None = None

    comparison: str | None = None


class TriageResult(BaseModel):

    suggested_group: TriageGroup

    treatment_priority: str

    color: str

    max_wait_minutes: int

    reevaluation_minutes: int | None

    protocol_name: str

    protocol_version: str

    rule_findings: list[RuleFinding]

    triggered_rules: list[str]

    red_flags: list[str]

    relevant_factors: list[str]

    missing_information: list[str]

    assessment_status: AssessmentStatus

    safety_warnings: list[str]

    requires_human_review: bool = True