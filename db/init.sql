
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


CREATE TABLE "department" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    orgid INT REFERENCES "organization"(id)
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    deptid INT REFERENCES "department"(id),
    orgid INT REFERENCES "organization"(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    usertype VARCHAR(50) CHECK (usertype IN ('employee', 'orgadmin', 'superadmin')) NOT NULL
);

CREATE TABLE "survey" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    orgid INT REFERENCES "organization"(id)
);

CREATE TABLE "question" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    scorefactor INT NOT NULL
);

CREATE TABLE "surveyquestions" (
    surveyid INT REFERENCES "survey"(id) ON DELETE CASCADE,
    questionid INT REFERENCES "question"(id) ON DELETE CASCADE,
    PRIMARY KEY (surveyid, questionid)
);

CREATE TABLE "questionscore" (
    employeeid INT REFERENCES "user"(id),
    questionid INT REFERENCES "question"(id),
    score INT NOT NULL,
    PRIMARY KEY (employeeid, questionid)
);

CREATE INDEX idx_user_orgid ON "user"(orgid);
CREATE INDEX idx_user_deptid ON "user"(deptid);
CREATE INDEX idx_survey_orgid ON "survey"(orgid);


INSERT INTO "organization" (name) VALUES ('MY-KPI');
INSERT INTO "organization" (name) VALUES ('INATEL');
INSERT INTO "organization" (name) VALUES ('4Intelligence');

INSERT INTO "department" (name, orgid) VALUES ('Geral', 1);
INSERT INTO "department" (name, orgid) VALUES ('Recursos Humanos', 2);
INSERT INTO "department" (name, orgid) VALUES ('Desenvolvimento', 2);
INSERT INTO "department" (name, orgid) VALUES ('Engenharia', 2);
INSERT INTO "department" (name, orgid) VALUES ('Recursos Dos Manos', 3);
INSERT INTO "department" (name, orgid) VALUES ('Limpeza', 3);
INSERT INTO "department" (name, orgid) VALUES ('Carcereiros', 3);

INSERT INTO "user" (name, deptid, orgid, email, password, usertype) VALUES ('Master Admin', 1, 1, 'admin@mykpi.online', 'admin', 'superadmin');
INSERT INTO "user" (name, deptid, orgid, email, password, usertype) VALUES ('Admin do INATEL ', 2, 2, 'admin@inatel.br', 'admin', 'orgadmin');
INSERT INTO "user" (name, deptid, orgid, email, password, usertype) VALUES ('Admin da 4Intelligence ', 3, 3, 'admin@4intelligence.com', 'admin', 'orgadmin');
