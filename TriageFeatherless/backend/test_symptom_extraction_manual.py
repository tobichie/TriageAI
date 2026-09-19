from app.triage.symptom_rules import (
    extract_symptom_names
)


def test(
    value: str
) -> None:

    print(
        f"\nInput:\n{value}"
    )


    print(
        "\nExtracted:"
    )


    print(

        extract_symptom_names(
            value
        )

    )


test(
    "chest pain"
)


test(
    "chest pain, shortness of breath"
)


test(
    "Patient has shortness of breath, "
    "Patient also has chest pain"
)


test(
    "shortness of breath chest pain"
)


test(
    "Patient reports heart palpitations "
    "and chest discomfort"
)