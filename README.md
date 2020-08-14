# Full-Stack Software Engineer Challenge

## Requirements

* Python >3.8
* Postgres >9

## Data model

![Image of Yaktocat](docs/MoroChallange.jpg)

### Entities

* Users - list of users
  * extensive_survey - true if user is included in extensive_survey program.
* Drivers - list of drives
* Rides - rides made by drive and user.
  * user_rate - rating for the ride given by user during survey.
* Surveys - list of surveys
* Questions - list of questions per each Surveys.
* AnswerOptions - list of optional answers for a question.
  * with_text - boolean field. if AnserOption allows free text.
* QuestionTypes - type of questions. can be: **multi**, **single**, **freetext**
* RideSurveys - list of answered surveys for ride.
* RideQuestions - list of answered question for RideSurveys entity.
* RideAnswers - list of answers for Question.
* AppConfig - Settings for application. Contains current survey_id used by default for survey if survey_id is not define explicitly.

## Endpoints

### / GET

Return webpage with rendered survey.

#### Query string arguments

* ride_id - the id of the ride, where we want to take survey about. Mandatory.
* survey_id - id of specific survey. If survey_id is not provided, we use **current_survey_id** value from **AppConfig** table.

#### Examples

* /?ride_id=1 - Show default (defined in AppConfig) survey regarding ride 1.
* /?ride_id=1&survey_id=1 - Show survey 1 for ride 1.

### /api/survey GET

Returns survey data in json format.

#### Query string arguments

* ride_id - the id of the ride, where we want to take survey about. Mandatory.
* survey_id - id of specific survey. If survey_id is not provided, we use **current_survey_id** value from **AppConfig** table.

#### Examples

* /api/survey?ride_id=1 - Show default (defined in AppConfig) survey regarding ride 1.
* /api/survey?ride_id=1&survey_id=1 - Show survey 1 for ride 1.

### /api/survey POST

Save survey answers.

#### Body Example

```
{
  "id": 1,
  "ride_id": 1,
  "user_rate": 2,
  "questions": [
    {"id": 3, "answers": [{"id": 4, "free_text": "TXT"}],}
  ],
}
 ```
 
 ### /api/reset-db GET
 
 Reset DB and load sample data.
 
 ## Sample Data
 
 Sample data is defined in [sample_data.sql](app/sample_data.sql)
 
 ### Users
 
 * user 1 - ask only user_rate
 * user 2 - ask extensive survey
 
 ### Surveys
 
 We have 2 surveys with ids: 1 and 2.
 
 ### Rides
 
 WE have 2 rides: id=1 for user id=1 and id=2 for user id=2
 
 ### AppConfig
 
 Contains: key='current_survey_id' value=1 - means: use survey_id 1 as default survey.
 
 ## Live site
 
 The live site is deployed to: https://ec2-18-185-39-90.eu-central-1.compute.amazonaws.com/
 
 ### Links to test
 
 * https://ec2-18-185-39-90.eu-central-1.compute.amazonaws.com/?ride_id=1 - show user_rate only (because user.extensive_survey=false) survey 1 (as defined in AppConfig) for ride 1 (user 1)
* https://ec2-18-185-39-90.eu-central-1.compute.amazonaws.com/?ride_id=2 - show full (because user.extensive_survey=true) survey 1 (as defined in AppConfig) for ride 2 (user 2)
* https://ec2-18-185-39-90.eu-central-1.compute.amazonaws.com/?ride_id=2&survey_id=2 - show full (because user.extensive_survey=true) survey 2 for ride 2 (user 2)

 ## Environment variables
 
 ### DB_URL
 
 Connection string to DB.
 
 Example: postgres://localhost/moro
 
 ### TEST_DB_URL
 
 Connection string to test DB.
 
 Example: postgres://localhost/moro_test
 

## Commands

```
FLASK_APP=app.main:app FLASK_ENV=development flask run -p 8080 > /tmp/moro-app.log 2>&1
```
