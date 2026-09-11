import pytest

from app.triage.normalization import (
    normalize_symptom_name
)


@pytest.mark.parametrize(

    "raw_symptom, expected",

    [

        (
            "Chest Pain",
            "chest_pain"
        ),

        (
            "CHEST PAIN",
            "chest_pain"
        ),

        (
            "chest-pain",
            "chest_pain"
        ),

        (
            "pain in chest",
            "chest_pain"
        ),

        (
            "difficulty breathing",
            "shortness_of_breath"
        ),

        (
            "HEADACHE",
            "headache"
        ),

        (
            "Something Unknown",
            "something_unknown"
        )

    ]

)

def test_normalize_symptom_name(

    raw_symptom,

    expected

):

    result = (
        normalize_symptom_name(
            raw_symptom
        )
    )


    assert result == expected