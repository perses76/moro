import pytest
from tests import helpers as hlp

pytestmark = pytest.mark.usefixtures("db")

def test_success(client):
    survey = hlp.Survey()
    question = hlp.Question(survey=survey)
    option = hlp.AnswerOption(question=question)
    ride = hlp.Ride()

    data = {
        "id": survey["id"],
        "ride_id": ride["id"],
        "user_rate": 1,
        "questions": [
            {"id": question["id"], "answers": [{"id": option["id"], "free_text": "TXT"}]}
        ]
    }
    response = client.post('/api/survey', json=data)
    assert response.status_code == 200
    assert response.get_json() == {"status": "OK"}
    ride_survey = hlp.db.fetchall("SELECT id, survey_id, ride_id FROM RideSurveys")[0]
    assert ride_survey == {
        "id": ride_survey["id"],
        "survey_id": survey["id"],
        "ride_id": ride["id"],
    }
    ride_question = hlp.db.fetchall("SELECT id, ride_survey_id, question_id FROM RideQuestions")[0]
    assert ride_question == {
        "id": ride_question["id"],
        "ride_survey_id": ride_survey["id"],
        "question_id": question["id"],
    }

    ride_answers = hlp.db.fetchall("SELECT id, ride_question_id, option_id, free_text FROM RideAnswers")
    assert len(ride_answers) == 1
    ride_answer = ride_answers[0]
    assert ride_answer == {
        "id": ride_answer["id"],
        "ride_question_id": ride_question["id"],
        "option_id": option["id"],
        "free_text": "TXT"
    }

    user_rate = hlp.db.fetchval("SELECT user_rate FROM Rides WHERE id=%s", [ride["id"]])
    assert user_rate == 1
