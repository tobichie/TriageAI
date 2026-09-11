"""
Prototype symptom rules.

IMPORTANT:

These rules are prototype software-development
rules and are NOT a validated clinical triage
protocol.
"""


CRITICAL_SYMPTOMS = {

    "unconsciousness": {

        "rule_id": (
            "SYMPTOM_UNCONSCIOUSNESS"
        ),

        "description": (
            "Reported unconsciousness."
        )

    },


    "cardiac_arrest": {

        "rule_id": (
            "SYMPTOM_CARDIAC_ARREST"
        ),

        "description": (
            "Reported cardiac arrest."
        )

    },


    "seizure": {

        "rule_id": (
            "SYMPTOM_SEIZURE"
        ),

        "description": (
            "Reported seizure."
        ),

    },



}

VERY_URGENT_SYMPTOMS = {

    "severe_bleeding": {

        "rule_id": (
            "SYMPTOM_SEVERE_BLEEDING"
        ),

        "description": (
            "Reported severe bleeding."
        )

    },


    "severe_breathing_difficulty": {

        "rule_id": (
            "SYMPTOM_SEVERE_BREATHING_DIFFICULTY"
        ),

        "description": (
            "Reported severe breathing difficulty."
        )

    }

}

URGENT_SYMPTOMS = {

    # Placeholder examples.

}

SYMPTOM_RULES = {

    "chest_pain": {

        "severity": {

            "very_urgent_min": 8,

            "urgent_min": 5,

            "normal_min": 1

        },


        "duration": {

            "urgent_min_minutes": 30

        }

    },


    "headache": {

        "severity": {

            "urgent_min": 8,

            "normal_min": 4,

            "not_urgent_min": 1

        }

    },


    "abdominal_pain": {

        "severity": {

            "very_urgent_min": 9,

            "urgent_min": 6,

            "normal_min": 3,

            "not_urgent_min": 1

        }

    },


    "shortness_of_breath": {

        "severity": {

            "very_urgent_min": 7,

            "urgent_min": 4,

            "normal_min": 1

        }

    }

}


SYMPTOM_ALIASES = {

    # Chest pain

    "chest pain": "chest_pain",

    "chest-pain": "chest_pain",

    "pain in chest": "chest_pain",

    "chest discomfort": "chest_pain",


    # Difficulty breathing

    "shortness of breath":
        "shortness_of_breath",

    "difficulty breathing":
        "shortness_of_breath",

    "trouble breathing":
        "shortness_of_breath",

    "breathlessness":
        "shortness_of_breath",


    # Headache

    "headache": "headache",

    "head pain": "headache",


    # Abdominal pain

    "abdominal pain":
        "abdominal_pain",

    "stomach pain":
        "abdominal_pain",

    "belly pain":
        "abdominal_pain",


    # Stroke-like symptoms

    "weakness":
        "weakness",

    "facial drooping":
        "facial_drooping",

    "slurred speech":
        "slurred_speech",

    "difficulty speaking":
        "slurred_speech",

    # critical symptoms

    "unconscious": "unconsciousness",

    "loss of consciousness": (
        "unconsciousness"
    ),

    "passed out": (
        "unconsciousness"
    ),

    "cardiac arrest": (
        "cardiac_arrest"
    ),

    "heart stopped": (
        "cardiac_arrest"
    ),

    "convulsion": (
        "seizure"
    ),

    "convulsions": (
        "seizure"
    ),

    "seizing": (
        "seizure"
    ),

    "severe bleeding": (
        "severe_bleeding"
    ),

    "heavy bleeding": (
        "severe_bleeding"
    ),

    "massive bleeding": (
        "severe_bleeding"
    ),


    "severe breathing difficulty": (
        "severe_breathing_difficulty"
    ),

    "cannot breathe": (
        "severe_breathing_difficulty"
    ),

    "extreme shortness of breath": (
        "severe_breathing_difficulty"
    ),

}