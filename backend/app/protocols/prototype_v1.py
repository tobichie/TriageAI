"""
Prototype triage protocol.

IMPORTANT:
The thresholds in this file are prototype
software-development values.

They are NOT a validated clinical protocol and
must not be used for real clinical decision-making
without appropriate clinical governance and validation.
"""


PROTOCOL_NAME = (
    "Prototype Triage Protocol"
)
PROTOCOL_VERSION = "1.0"


VITAL_SIGN_THRESHOLDS = {

    "oxygen_saturation": {

        "critical_max": 85,

        "very_urgent_max": 90,

        "urgent_max": 94

    },


    "heart_rate": {

    "critical_high_min": 150,

    "very_urgent_high_min": 130,

    "urgent_high_min": 110,

    "critical_low_max": 40,

    "very_urgent_low_max": 50,

    "urgent_low_max": 55

},

    "blood_pressure": {

        "critical_systolic_low_max": 80,

        "very_urgent_systolic_low_max": 90,

        "urgent_systolic_low_max": 100,


        "critical_systolic_high_min": 220,

        "very_urgent_systolic_high_min": 180,

        "urgent_systolic_high_min": 160

    }

}