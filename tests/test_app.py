import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_activities = deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(original_activities)


def test_get_activities():
    client = TestClient(app)
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_success():
    client = TestClient(app)
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.text


def test_signup_for_activity_duplicate():
    email = "michael@mergington.edu"
    client = TestClient(app)
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert "Student already signed up" in response.text


def test_signup_for_activity_not_found():
    client = TestClient(app)
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.text


def test_remove_participant_success():
    email = "lucy@mergington.edu"
    client = TestClient(app)
    response = client.delete("/activities/Drama Club/participants", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email} from Drama Club" in response.text


def test_remove_participant_not_found():
    email = "notfound@mergington.edu"
    client = TestClient(app)
    response = client.delete("/activities/Drama Club/participants", params={"email": email})
    assert response.status_code == 404
    assert "Participant not found" in response.text
