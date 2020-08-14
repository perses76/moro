DROP TABLE IF EXISTS AppConfig;
DROP TABLE IF EXISTS RideAnswers;
DROP TABLE IF EXISTS RideQuestions;
DROP TABLE IF EXISTS RideSurveys;
DROP TABLE IF EXISTS AnswerOptions;
DROP TABLE IF EXISTS Questions;
DROP TABLE IF EXISTS QuestionTypes;
DROP TABLE IF EXISTS Surveys;

DROP TABLE IF EXISTS Rides;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Drivers;


CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    extensive_survey BOOLEAN NOT NULL DEFAULT(false)
);

CREATE TABLE Drivers (
    id SERIAL PRIMARY KEY
);

CREATE TABLE Rides (
    id SERIAL PRIMARY KEY,
    user_id int NOT NULL,
    driver_id int NOT NULL,
    user_rate int NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (driver_id) REFERENCES Drivers(id),
    UNIQUE (driver_id, user_id)
);

CREATE TABLE Surveys (
    id SERIAL PRIMARY KEY,
    title varchar(100)
);

CREATE TABLE QuestionTypes (
    code varchar(100) NOT NULL PRIMARY KEY
);

CREATE TABLE Questions (
    id SERIAL PRIMARY KEY,
    title varchar(100) NOT NULL,
    question_type varchar(100) NOT NULL,
    survey_id int NOT NULL,
    FOREIGN KEY (question_type) REFERENCES QuestionTypes(code),
    FOREIGN KEY (survey_id) REFERENCES Surveys(id)
);

CREATE TABLE AnswerOptions (
    id SERIAL PRIMARY KEY,
    title varchar(100) NOT NULL,
    question_id int NOT NULL,
    with_text BOOLEAN NOT NULL DEFAULT(false),
    FOREIGN KEY (question_id) REFERENCES Questions(id)
);

CREATE TABLE RideSurveys (
    id SERIAL PRIMARY KEY,
    ride_id int NOT NULL,
    survey_id int NOT NULL,
    FOREIGN KEY (ride_id) REFERENCES Rides(id),
    FOREIGN KEY (survey_id) REFERENCES Surveys(id),
    UNIQUE (ride_id, survey_id)
);

CREATE TABLE RideQuestions (
    id SERIAL PRIMARY KEY,
    ride_survey_id int NOT NULL,
    question_id int NOT NULL,
    FOREIGN KEY (ride_survey_id) REFERENCES RideSurveys(id),
    FOREIGN KEY (question_id) REFERENCES Questions(id),
    UNIQUE (ride_survey_id, question_id)
);

CREATE TABLE RideAnswers (
    id SERIAL PRIMARY KEY,
    ride_question_id int NOT NULL,
    option_id int NOT NULL,
    free_text TEXT NULL,
    FOREIGN KEY (ride_question_id) REFERENCES RideQuestions(id),
    FOREIGN KEY (option_id) REFERENCES AnswerOptions(id),
    UNIQUE (ride_question_id, option_id)
);

CREATE TABLE AppConfig (
    key varchar(100) NOT NULL PRIMARY KEY,
    value TEXT NULL
)
