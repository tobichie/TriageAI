from enum import Enum

from pydantic import BaseModel

from app.triage.priorities import TriageGroup


class RuleCategory(str, Enum):

    RED_FLAG = "red_flag"

    VITAL_SIGN = "vital_sign"

    SYMPTOM = "symptom"


class RuleFinding(BaseModel):

    rule_id: str

    category: RuleCategory

    description: str

    suggested_group: TriageGroup


class TriageResult(BaseModel):

    suggested_group: TriageGroup

    treatment_priority: str

    color: str

    max_wait_minutes: int

    reevaluation_minutes: int | None

    triggered_rules: list[str]

    red_flags: list[str]

    relevant_factors: list[str]

    missing_information: list[str]

    requires_human_review: bool = True