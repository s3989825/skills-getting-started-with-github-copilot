from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_expected_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()

    assert "Chess Club" in body
    assert body["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )
    assert body["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_participant_and_rejects_duplicates():
    activity_name = "Chess Club"
    email = "newstudent@example.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert duplicate_response.status_code == 400
    assert duplicate_response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_unregister_participant_removes_student_and_rejects_missing_participant():
    activity_name = "Chess Club"
    email = "newstudent@example.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    missing_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    assert missing_response.status_code == 404
    assert missing_response.json() == {"detail": "Participant not found"}
