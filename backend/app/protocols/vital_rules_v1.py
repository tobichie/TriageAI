"""
Vital sign rules for TriageAI Prototype Protocol v1.

IMPORTANT:

These rules are prototype decision-support rules.

They are NOT a validated clinical protocol and are
NOT a complete implementation of the Manchester
Triage System.

They must not be used for real-world clinical
decision making.
"""


from app.triage.priorities import (
    TriageGroup
)


VITAL_RULES = {

    "oxygen_saturation": [

        {
            "rule_id": (
                "VITAL_SPO2_CRITICAL"
            ),

            "operator": (
                "less_than_or_equal"
            ),

            "threshold": 85,

            "suggested_group": (
                TriageGroup.IMMEDIATE
            ),

            "description": (
                "Critically low oxygen saturation."
            )
        },

        {
            "rule_id": (
                "VITAL_SPO2_LOW"
            ),

            "operator": (
                "less_than_or_equal"
            ),

            "threshold": 90,

            "suggested_group": (
                TriageGroup.VERY_URGENT
            ),

            "description": (
                "Low oxygen saturation."
            )
        }

    ],


    "heart_rate": [

        {
            "rule_id": (
                "VITAL_HR_VERY_HIGH"
            ),

            "operator": (
                "greater_than_or_equal"
            ),

            "threshold": 150,

            "suggested_group": (
                TriageGroup.VERY_URGENT
            ),

            "description": (
                "Very high heart rate."
            )
        },

        {
            "rule_id": (
                "VITAL_HR_HIGH"
            ),

            "operator": (
                "greater_than_or_equal"
            ),

            "threshold": 120,

            "suggested_group": (
                TriageGroup.URGENT
            ),

            "description": (
                "High heart rate."
            )
        }

    ]

}