from app.models.patient import (
    PatientData,
    VitalSigns
)

from app.triage.priorities import (
    TriageGroup
)

from app.triage.vital_rules import (
    evaluate_vital_signs
)


def create_patient(

    heart_rate=None,

    oxygen_saturation=None,

    systolic_bp=None

) -> PatientData:

    return PatientData(

        vital_signs=VitalSigns(

            heart_rate=heart_rate,

            oxygen_saturation=(
                oxygen_saturation
            ),

            systolic_bp=systolic_bp
        )
    )

# --------------------------------
# BLOOD PRESSURE
# --------------------------------

def test_critical_low_blood_pressure():

    patient = create_patient(
        systolic_bp=70
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_BP_CRITICAL_LOW"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.IMMEDIATE

        for finding in findings
    )


def test_very_urgent_low_blood_pressure():

    patient = create_patient(
        systolic_bp=85
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_BP_VERY_URGENT_LOW"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.VERY_URGENT

        for finding in findings
    )


def test_urgent_low_blood_pressure():

    patient = create_patient(
        systolic_bp=95
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_BP_URGENT_LOW"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.URGENT

        for finding in findings
    )


def test_critical_high_blood_pressure():

    patient = create_patient(
        systolic_bp=230
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_BP_CRITICAL_HIGH"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.IMMEDIATE

        for finding in findings
    )


def test_very_urgent_high_blood_pressure():

    patient = create_patient(
        systolic_bp=190
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_BP_VERY_URGENT_HIGH"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.VERY_URGENT

        for finding in findings
    )


def test_urgent_high_blood_pressure():

    patient = create_patient(
        systolic_bp=170
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_BP_URGENT_HIGH"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.URGENT

        for finding in findings
    )

# --------------------------------
# OXYGEN SATURATION
# --------------------------------

def test_critical_oxygen_saturation():

    patient = create_patient(
        oxygen_saturation=80
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_SPO2_CRITICAL"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.IMMEDIATE

        for finding in findings
    )


def test_very_urgent_oxygen_saturation():

    patient = create_patient(
        oxygen_saturation=88
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_SPO2_VERY_URGENT"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.VERY_URGENT

        for finding in findings
    )


def test_urgent_oxygen_saturation():

    patient = create_patient(
        oxygen_saturation=93
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == "VITAL_SPO2_URGENT"

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.URGENT

        for finding in findings
    )


# --------------------------------
# HEART RATE - HIGH
# --------------------------------

def test_critical_high_heart_rate():

    patient = create_patient(
        heart_rate=160
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == (
            "VITAL_HEART_RATE_CRITICAL_HIGH"
        )

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.IMMEDIATE

        for finding in findings
    )


def test_very_urgent_high_heart_rate():

    patient = create_patient(
        heart_rate=140
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == (
            "VITAL_HEART_RATE_VERY_URGENT_HIGH"
        )

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.VERY_URGENT

        for finding in findings
    )


def test_urgent_high_heart_rate():

    patient = create_patient(
        heart_rate=115
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == (
            "VITAL_HEART_RATE_URGENT_HIGH"
        )

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.URGENT

        for finding in findings
    )


# --------------------------------
# HEART RATE - LOW
# --------------------------------

def test_critical_low_heart_rate():

    patient = create_patient(
        heart_rate=35
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == (
            "VITAL_HEART_RATE_CRITICAL_LOW"
        )

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.IMMEDIATE

        for finding in findings
    )


def test_very_urgent_low_heart_rate():

    patient = create_patient(
        heart_rate=45
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == (
            "VITAL_HEART_RATE_VERY_URGENT_LOW"
        )

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.VERY_URGENT

        for finding in findings
    )


def test_urgent_low_heart_rate():

    patient = create_patient(
        heart_rate=52
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert any(

        finding.rule_id
        == (
            "VITAL_HEART_RATE_URGENT_LOW"
        )

        for finding in findings
    )


    assert any(

        finding.suggested_group
        == TriageGroup.URGENT

        for finding in findings
    )


# --------------------------------
# NORMAL VALUES
# --------------------------------

def test_normal_vital_signs_produce_no_findings():

    patient = create_patient(

        heart_rate=75,

        oxygen_saturation=98
    )


    findings = evaluate_vital_signs(
        patient
    )


    assert findings == []