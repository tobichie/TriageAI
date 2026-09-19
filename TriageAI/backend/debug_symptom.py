from app.triage.normalization import (
    normalize_text,
)

from app.triage.symptom_rules import (
    resolve_symptom_name
)

from app.protocols.symptom_rules_v1 import (
    SYMPTOM_RULES
)


raw_name = "heart attack"


normalized_name = (
    normalize_text(
        raw_name
    )
)


resolved_name = (
    resolve_symptom_name(
        normalized_name
    )
)


print(
    "Raw:"
)

print(
    raw_name
)


print()


print(
    "Normalized:"
)

print(
    normalized_name
)


print()


print(
    "Resolved:"
)

print(
    resolved_name
)


print()


print(
    "In SYMPTOM_RULES:"
)

print(
    resolved_name
    in SYMPTOM_RULES
)


print()


if (
    resolved_name
    in SYMPTOM_RULES
):

    print(
        "Rule:"
    )

    print(
        SYMPTOM_RULES[
            resolved_name
        ]
    )