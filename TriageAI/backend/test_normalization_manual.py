from app.triage.normalization import (
    normalize_symptom_name
)


TEST_SYMPTOMS = [

    "Chest Pain",

    "CHEST PAIN",

    "chest-pain",

    "pain in chest",

    "Shortness of Breath",

    "difficulty breathing",

    "HEADACHE",

    "head pain",

    "Something Completely Unknown"
]


for symptom in TEST_SYMPTOMS:

    normalized = (
        normalize_symptom_name(
            symptom
        )
    )


    print(

        f"{symptom} "
        f"-> "
        f"{normalized}"

    )