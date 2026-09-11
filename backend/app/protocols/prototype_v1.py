"""
Prototype triage protocol.

IMPORTANT:
The thresholds in this file are prototype
software-development values.

They are NOT a validated clinical protocol and
must not be used for real clinical decision-making
without appropriate clinical governance and validation.
"""


PROTOCOL_NAME = "Prototype Triage Protocol"

PROTOCOL_VERSION = "1.0"


VITAL_SIGN_THRESHOLDS = {

    "oxygen_saturation": {

        "critical_max": 85

    },


    "heart_rate": {

        "critical_min": 160

    },


    "blood_pressure": {

        "enabled": False

    }

}