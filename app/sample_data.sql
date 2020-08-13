INSERT INTO Users(id, extensive_survey) VALUES
(1, false),
(2, true);

INSERT INTO Drivers(id) VALUES
(1);

INSERT INTO Rides(user_id, driver_id) VALUES
(1, 1),
(2, 1);


INSERT INTO Surveys(id, title) VALUES
(1, 'Survey 1'),
(2, 'Survey 2');

INSERT INTO QuestionTypes(code) VALUES
('multi'),
('single'),
('freetext');


INSERT INTO Questions(id, title, question_type, survey_id) VALUES
(1, 'Road Behavior', 'single', 1),
(2, 'Car Interior', 'multi', 1),
(3, 'Other', 'freetext', 1);

INSERT INTO AnswerOptions(id, title, question_id, with_text) VALUES
(1, 'Aggresive', 1, false),
(2, 'Smooth', 1, false),
(3, 'Other', 1, true),

(4, 'Clean', 2, false),
(5, 'Adequate legroom', 2, false),
(6, 'Clean', 2, false),

(7, 'Anything else you would like to share about your ride?', 3, false);
