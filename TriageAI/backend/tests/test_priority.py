from app.triage.priorities import (
    TriageGroup,
    TRIAGE_GROUPS
)


group = TriageGroup.VERY_URGENT

print(group)

print(TRIAGE_GROUPS[group])