# Full-Stack Software Engineer Challenge

## Requirements

* Python >3.8
* Postgres >9

## Data model

![Image of Yaktocat](docs/MoroChallange.jpg)

### Entities

* Users - list of users
* Drivers - list of drives
* Rides - rides made by drive and user.
* Surveys - list of surveys
* Questions - list of questions per each Surveys.
* AnswerOptions - list of optional answers for a question.
  * with_text - boolean field. if AnserOption allows free text.
* QuestionTypes - type of questions. can be: **multi**, **single**, **freetext**
* RideSurveys - list of answered surveys for ride.
* RideQuestions - list of answered question for RideSurveys entity.
* RideAnswers - list of answers for Question.
* AppConfig - Settings for application. Contains current survey_id used by default for survey if survey_id is not define explicitly.


## Run

```
FLASK_APP=app.main:app FLASK_ENV=development flask run -p 8080 > /tmp/moro-app.log 2>&1
```
