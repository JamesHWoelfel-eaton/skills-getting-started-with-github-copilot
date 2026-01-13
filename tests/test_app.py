from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "teststudent@example.com"

    # Ensure the participant is not present (ignore errors)
    client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    body = res.json()
    assert "Signed up" in body.get("message", "")

    # Verify participant appears
    res2 = client.get("/activities")
    assert res2.status_code == 200
    participants = res2.json()[activity]["participants"]
    assert email in participants

    # Unregister
    res3 = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert res3.status_code == 200

    # Verify participant removed
    res4 = client.get("/activities")
    participants2 = res4.json()[activity]["participants"]
    assert email not in participants2