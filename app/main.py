"""Main web app module."""

from itertools import groupby

import flask

from . import cli, db

app = flask.Flask(__name__)


@app.route("/")
def index():
    """Index page."""
    return flask.render_template("index.html")


def _format_options(options):
    """Format answer option to return in survey response."""
    return [
        {"id": op["id"], "title": op["title"], "with_text": op["with_text"],}
        for op in options
    ]


def make_error(message):
    """Generate error HTTP response."""
    return {"status": "ERROR", "message": message}, 400


@app.route("/api/survey")
def survey_handler():
    """Survey handler."""
    ride_id = flask.request.args["ride_id"]
    survey_id = flask.request.args.get("survey_id")
    with db.connect() as conn:
        rides = db.fetchall(
            "SELECT id, user_id, driver_id FROM Rides WHERE id=%s", [ride_id]
        )
        if not rides:
            return make_error(f"raid with ride_id={ ride_id } is not found")
        ride = rides[0]

        current_survey_id = survey_id
        if not current_survey_id:
            current_survey_id = db.fetchval(
                "SELECT value FROM AppConfig WHERE key='current_survey_id'"
            )

        if not current_survey_id:
            return make_error(
                "survey_id was not provided and "
                "not defined in AppConfig for key 'current_survey_id'"
            )

        surveys = db.fetchall(
            "SELECT id, title FROM Surveys WHERE id= %s",
            params=[current_survey_id],
            conn=conn,
        )
        if not surveys:
            return make_error(f"Can not find survey with id: {current_survey_id}")
        survey = surveys[0]

        ride_survey_id = db.fetchval(
            "SELECT id FROM RideSurveys WHERE survey_id=%s and ride_id = %s",
            [survey["id"], ride["id"]],
        )
        if ride_survey_id:
            return make_error(
                f"The survey: {survey['id']} for ride: {ride['id']} has been taken already."
            )

        user = db.fetchall(
            "SELECT id, extensive_survey FROM Users WHERE id=%s", [ride["user_id"]]
        )[0]
        if user["extensive_survey"]:
            questions = db.fetchall(
                "SELECT id, title, question_type as type FROM Questions WHERE survey_id = %s",
                [survey["id"]],
            )
            options = db.fetchall(
                "SELECT ao.id, ao.title, ao.question_id, ao.with_text FROM AnswerOptions ao "
                "INNER JOIN Questions q ON ao.question_id = q.id WHERE q.survey_id = %s;",
                [survey["id"]],
            )
            options = sorted(options, key=lambda obj: obj["question_id"])
            options_grouped = {
                key: _format_options(group)
                for key, group in groupby(options, key=lambda obj: obj["question_id"])
            }
            for question in questions:
                question["options"] = options_grouped[question["id"]]
            survey["questions"] = questions
        else:
            survey["questions"] = []
        survey["user_rate"] = 3
    return flask.jsonify({"status": "OK", "survey": survey})


@app.route("/api/survey", methods=["POST"])
def save_survey():
    """Save survey in DB."""
    data = flask.request.get_json()
    db.execute(
        "UPDATE Rides SET user_rate = %s WHERE id=%s",
        [data["user_rate"], data["ride_id"]],
    )
    ride_survey_id = db.insert(
        "INSERT INTO RideSurveys (survey_id, ride_id) VALUES (%s, %s) RETURNING id;",
        [data["id"], data["ride_id"]],
    )
    for question in data["questions"]:
        ride_question_id = db.insert(
            "INSERT INTO RideQuestions (ride_survey_id, question_id) VALUES (%s, %s) RETURNING id;",
            [ride_survey_id, question["id"]],
        )
        for answer in question["answers"]:
            db.execute(
                "INSERT INTO RideAnswers (ride_question_id, option_id, free_text) "
                "VALUES (%s, %s, %s)",
                [ride_question_id, answer["id"], answer.get("free_text")],
            )
    return {"status": "OK"}


@app.cli.command("init-db")
def init_db():
    """Create Schema and load test data."""
    return cli.init_db()
