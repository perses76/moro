import pytest
from tests import helpers as hlp

pytestmark = pytest.mark.usefixtures("db")

def test_success_extensive_survey(client):
    """Check response of extensive_survey."""
    survey = hlp.Survey(id=1, title="Survey1")
    question = hlp.Question(id=1, title="Question1", question_type="single", survey=survey)
    option = hlp.AnswerOption(id=1, title="Option1", question=question, with_text=True)
    user = hlp.User(extensive_survey=True)
    ride = hlp.Ride(user=user)
    response = client.get("api/survey", query_string={"ride_id": ride["id"], "survey_id": survey["id"]})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "OK"
    assert data["survey"] == {
        "id": survey["id"],
        "title": survey["title"],
        "user_rate": 3,
        "questions": [
            {
                "id": question["id"],
                "title": question["title"],
                "type": question["question_type"],
                "options": [
                    {"id": option["id"], "title": option["title"], "with_text": option["with_text"]}
                ]
            }
        ]
    }


def test_success_not_extensive_survey(client):
    """Check response of NOT extensive_survey."""
    survey = hlp.Survey(id=1, title="Survey1")
    question = hlp.Question(id=1, title="Question1", question_type="single", survey=survey)
    option = hlp.AnswerOption(id=1, title="Option1", question=question, with_text=True)
    user = hlp.User(extensive_survey=False)
    ride = hlp.Ride(user=user)
    response = client.get("api/survey", query_string={"ride_id": ride["id"], "survey_id": survey["id"]})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "OK"
    assert data["survey"] == {
        "id": survey["id"],
        "title": survey["title"],
        "user_rate": 3,
        "questions": []
    }


def test_error_no_ride(client):
    """If ride does not exists, return error."""
    survey = hlp.Survey()
    response = client.get("api/survey", query_string={"ride_id": 555, "survey_id": survey["id"]})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "ERROR"


def test_error_no_survey(client):
    """If survey does not exists return error."""
    ride = hlp.Ride()
    response = client.get("api/survey", query_string={"ride_id": ride["id"], "survey_id": 555})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "ERROR"


def test_error_no_survey_id_provided(client):
    """Return error if no survey_id provided in query."""
    ride = hlp.Ride()
    response = client.get("api/survey", query_string={"ride_id": ride["id"]})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "ERROR"


def test_error_survey_defined_in_config(client):
    """Define current survey in AppConfig."""
    ride = hlp.Ride()
    survey = hlp.Survey()
    hlp.AppConfig(key="current_survey_id", value=survey["id"])
    response = client.get("api/survey", query_string={"ride_id": ride["id"]})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "OK"

def test_survey_for_ride_already_taken(client):
    survey = hlp.Survey()
    ride = hlp.Ride()
    hlp.RideSurvey(survey=survey, ride=ride)
    response = client.get("api/survey", query_string={"ride_id": ride["id"], "survey_id": survey["id"]})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "ERROR"
