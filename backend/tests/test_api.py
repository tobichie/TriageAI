from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_triage():

    patient = {

        "age": 30,

        "symptoms": [],

        "vital_signs": {

            "heart_rate": 80,

            "systolic_bp": 120,

            "diastolic_bp": 80,

            "oxygen_saturation": 98
        },

        "clinical_context": (
            "Prototype API test"
        )
    }


    response = client.post(
        "/triage",
        json=patient
    )


    assert response.status_code == 200


    data = response.json()


    assert data["suggested_group"] == 5

    assert data["color"] == "blue"

    assert (
        data["requires_human_review"]
        is True
    )