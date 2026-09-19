import re

from app.protocols.symptom_rules_v1 import (
    SYMPTOM_ALIASES
)

def normalize_text(
    value: str
) -> str:

    return (
        value
        .strip()
        .lower()
    )


def normalize_symptom_name(
    symptom_name: str
) -> str:

    normalized = (
        symptom_name
        .strip()
        .lower()
    )


    normalized = (
        normalized.replace(
            "-",
            " "
        )
    )


    normalized = re.sub(
        r"\s+",
        " ",
        normalized
    )


    if normalized in SYMPTOM_ALIASES:

        return SYMPTOM_ALIASES[
            normalized
        ]


    return (
        normalized.replace(
            " ",
            "_"
        )
    )