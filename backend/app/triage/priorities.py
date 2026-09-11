from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class TriageGroup(IntEnum):
    """
    Five-level triage priority system.

    Group 1 = highest urgency
    Group 5 = lowest urgency.
    """

    IMMEDIATE = 1
    VERY_URGENT = 2
    URGENT = 3
    NORMAL = 4
    NOT_URGENT = 5


@dataclass(frozen=True)
class TriageGroupInfo:

    group: TriageGroup

    treatment_priority: str

    color: str

    max_wait_minutes: int

    reevaluation_minutes: Optional[int]


TRIAGE_GROUPS = {

    TriageGroup.IMMEDIATE:

        TriageGroupInfo(
            group=TriageGroup.IMMEDIATE,
            treatment_priority="Sofort",
            color="red",
            max_wait_minutes=0,
            reevaluation_minutes=None
        ),


    TriageGroup.VERY_URGENT:

        TriageGroupInfo(
            group=TriageGroup.VERY_URGENT,
            treatment_priority="Sehr dringend",
            color="orange",
            max_wait_minutes=10,
            reevaluation_minutes=10
        ),


    TriageGroup.URGENT:

        TriageGroupInfo(
            group=TriageGroup.URGENT,
            treatment_priority="Dringend",
            color="yellow",
            max_wait_minutes=30,
            reevaluation_minutes=30
        ),


    TriageGroup.NORMAL:

        TriageGroupInfo(
            group=TriageGroup.NORMAL,
            treatment_priority="Normal",
            color="green",
            max_wait_minutes=90,
            reevaluation_minutes=90
        ),


    TriageGroup.NOT_URGENT:

        TriageGroupInfo(
            group=TriageGroup.NOT_URGENT,
            treatment_priority="Nicht dringend",
            color="blue",
            max_wait_minutes=120,
            reevaluation_minutes=120
        )
}