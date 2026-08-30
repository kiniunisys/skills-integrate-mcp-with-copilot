from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_anonymous_users_cannot_manage_activity_registrations():
    response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Teacher login required"

    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Teacher login required"


def test_teacher_can_login_and_manage_registrations():
    login_response = client.post(
        "/login",
        json={"username": "teacher", "password": "school123"},
    )

    assert login_response.status_code == 200
    assert login_response.json()["message"] == "Logged in successfully"

    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@example.com"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@example.com for Chess Club"

    response = client.delete(
        "/activities/Chess Club/unregister?email=newstudent@example.com"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered newstudent@example.com from Chess Club"
