
DROP TABLE IF EXISTS "questionscore";
DROP TABLE IF EXISTS "surveyquestions";
DROP TABLE IF EXISTS "question";
DROP TABLE IF EXISTS "survey";
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "department";
DROP TABLE IF EXISTS "organization";


CREATE TABLE "organization" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO "organization" (name) VALUES ('Org 1');

CREATE TABLE "department" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    orgId INT REFERENCES "organization"(id)
);

INSERT INTO "department" (name, orgId) VALUES ('Dept 1', 1);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    deptId INT REFERENCES "department"(id),
    orgId INT REFERENCES "organization"(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    usertype VARCHAR(50) CHECK (usertype IN ('employee', 'admin')) NOT NULL
);

CREATE TABLE "survey" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    orgId INT REFERENCES "organization"(id)
);

CREATE TABLE "question" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE "surveyquestions" (
    surveyId INT REFERENCES "survey"(id) ON DELETE CASCADE,
    questionId INT REFERENCES "question"(id) ON DELETE CASCADE,
    PRIMARY KEY (surveyId, questionId)
);

CREATE TABLE "questionscore" (
    employeeId INT REFERENCES "user"(id),
    questionId INT REFERENCES "question"(id),
    score INT NOT NULL,
    PRIMARY KEY (employeeId, questionId)
);

CREATE INDEX idx_user_orgId ON "user"(orgId);
CREATE INDEX idx_user_deptId ON "user"(deptId);
CREATE INDEX idx_survey_orgId ON "survey"(orgId);
