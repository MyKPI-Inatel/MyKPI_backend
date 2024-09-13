# drop tables
DROP TABLE IF EXISTS QuestionScore;
DROP TABLE IF EXISTS SurveyQuestions;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS Survey;
DROP TABLE IF EXISTS "User";
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Organization;


CREATE TABLE organization (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    orgId INT REFERENCES Organization(id)
);

CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    deptId INT REFERENCES Department(id),
    orgId INT REFERENCES Organization(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('employee', 'admin')) NOT NULL
);

CREATE TABLE survey (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    orgId INT REFERENCES Organization(id)
);

CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE surveyquestions (
    surveyId INT REFERENCES Survey(id) ON DELETE CASCADE,
    questionId INT REFERENCES Question(id) ON DELETE CASCADE,
    PRIMARY KEY (surveyId, questionId)
);

CREATE TABLE questionscore (
    employeeId INT REFERENCES "User"(id),
    questionId INT REFERENCES Question(id),
    score INT NOT NULL,
    PRIMARY KEY (employeeId, questionId)
);

CREATE INDEX idx_user_orgId ON "User"(orgId);
CREATE INDEX idx_user_deptId ON "User"(deptId);
CREATE INDEX idx_survey_orgId ON Survey(orgId);
