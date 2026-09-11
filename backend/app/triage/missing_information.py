from app.models.patient import PatientData


def detect_missing_information(
    patient: PatientData
) -> list[str]:

    missing = []


    if patient.age is None:

        missing.append("age")


    if not patient.symptoms:

        missing.append("symptoms")


    if patient.vital_signs.heart_rate is None:

        missing.append("heart_rate")


    if patient.vital_signs.systolic_bp is None:

        missing.append("systolic_bp")


    if patient.vital_signs.diastolic_bp is None:

        missing.append("diastolic_bp")


    if patient.vital_signs.oxygen_saturation is None:

        missing.append(
            "oxygen_saturation"
        )


    return missing