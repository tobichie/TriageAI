from enum import Enum


class AssessmentStatus(str, Enum):
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    REQUIRES_REVIEW = "requires_review"