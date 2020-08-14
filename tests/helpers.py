from app import db
import factory


class Survey(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f"Survey {n}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO Surveys (id, title) VALUES (%s, %s);"
        db.execute(sql, [kwargs["id"], kwargs["title"]])
        return kwargs


class Question(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f"Question {n}")
    survey = factory.SubFactory(Survey)
    question_type = "multi"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO Questions (id, title, survey_id, question_type) VALUES (%s, %s, %s, %s);"
        db.execute(sql, [
            kwargs["id"], kwargs["title"], kwargs["survey"]["id"], kwargs["question_type"]
        ])
        return kwargs


class AnswerOption(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: f"Option {n}")
    question = factory.SubFactory(Question)
    with_text = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO AnswerOptions (id, title, question_id, with_text) VALUES (%s, %s, %s, %s);"
        db.execute(sql, [
            kwargs["id"], kwargs["title"], kwargs["question"]["id"], kwargs["with_text"]
        ])
        return kwargs


class User(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)
    extensive_survey = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO Users (id, extensive_survey) VALUES (%s, %s);"
        db.execute(sql, [kwargs["id"], kwargs["extensive_survey"]])
        return kwargs


class Driver(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO Drivers (id) VALUES (%s);"
        db.execute(sql, [kwargs["id"]])
        return kwargs


class Ride(factory.Factory):
    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(User)
    driver = factory.SubFactory(Driver)
    user_rate = 2

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO Rides (id, user_id, driver_id, user_rate) VALUES (%s, %s, %s, %s);"
        db.execute(sql,
            [kwargs["id"], kwargs["user"]["id"], kwargs["driver"]["id"], kwargs["user_rate"]])
        return kwargs


class AppConfig(factory.Factory):
    class Meta:
        model = dict

    key = factory.Sequence(lambda n: f"key_{n}")
    value = factory.Sequence(lambda n: f"value_{n}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO AppConfig (key, value) VALUES (%s, %s);"
        db.execute(sql,
            [kwargs["key"], kwargs["value"]]
        )
        return kwargs


class RideSurvey(factory.Factory):
    class Meta:
        model = dict

    survey = factory.SubFactory(Survey)
    ride = factory.SubFactory(Ride)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        sql = "INSERT INTO RideSurveys (survey_id, ride_id) VALUES (%s, %s);"
        db.execute(sql,
            [kwargs["survey"]["id"], kwargs["ride"]["id"]]
        )
        return kwargs
