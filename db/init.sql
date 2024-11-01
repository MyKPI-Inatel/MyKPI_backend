
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

/*
ADDING ORGS
*/
INSERT INTO "organization" (name) VALUES ('MY-KPI');        -- id = 1
INSERT INTO "organization" (name) VALUES ('INATEL');        -- id = 2
INSERT INTO "organization" (name) VALUES ('4Intelligence'); -- id = 3

/*
ADDING DEPARTMENTS
*/
INSERT INTO "department" (name, orgid) VALUES ('Geral', 1);             -- id = 1 / org = MY-KPI
INSERT INTO "department" (name, orgid) VALUES ('Recursos Humanos', 2);  -- id = 2 / org = INATEL
INSERT INTO "department" (name, orgid) VALUES ('Desenvolvimento', 2);   -- id = 3 / org = INATEL
INSERT INTO "department" (name, orgid) VALUES ('Engenharia', 2);        -- id = 4 / org = INATEL
INSERT INTO "department" (name, orgid) VALUES ('Recursos Humanos', 3);  -- id = 5 / org = 4Intelligence
INSERT INTO "department" (name, orgid) VALUES ('Limpeza', 3);           -- id = 6 / org = 4Intelligence
INSERT INTO "department" (name, orgid) VALUES ('Desenvolvimento', 3);   -- id = 7 / org = 4Intelligence

/*
ADDING USERS
*/
-- ORGANIZATIION MY-KPI
INSERT INTO "user" (name, deptid, orgid, email, password, usertype)  -- id = 1 / superadmin / dept = Geral
VALUES ('Master Admin', 1, 1, 'admin@mykpi.online', '$argon2id$v=19$m=65536,t=3,p=4$0NMBnpJi+zMDOXbEQbinEA$CReTuQFvaMzh9+50m8Bs9n+nCNKbaPfS+2rvENkqbn8', 'superadmin');
-- ORGANIZATION INATEL
INSERT INTO "user" (name, deptid, orgid, email, password, usertype)  -- id = 2 / orgadmin / dept = Recursos Humanos
VALUES ('Admin do INATEL ', 2, 2, 'admin@inatel.br', '$argon2id$v=19$m=65536,t=3,p=4$0NMBnpJi+zMDOXbEQbinEA$CReTuQFvaMzh9+50m8Bs9n+nCNKbaPfS+2rvENkqbn8', 'orgadmin');
INSERT INTO "user" (name, deptid, orgid, email, password, usertype)  -- id = 3 / employee / dept = Desenvolvimento
VALUES ('Pedro', 4, 2, 'dev@inatel.br', '$argon2id$v=19$m=65536,t=3,p=4$0NMBnpJi+zMDOXbEQbinEA$CReTuQFvaMzh9+50m8Bs9n+nCNKbaPfS+2rvENkqbn8', 'employee');
-- ORGANIZATION 4INTELLIGENCE
INSERT INTO "user" (name, deptid, orgid, email, password, usertype)  -- id = 4 / orgadmin / dept = Recursos Humanos
VALUES ('Admin da 4Intelligence ', 3, 3, 'admin@4intelligence.com', '$argon2id$v=19$m=65536,t=3,p=4$0NMBnpJi+zMDOXbEQbinEA$CReTuQFvaMzh9+50m8Bs9n+nCNKbaPfS+2rvENkqbn8', 'orgadmin');
INSERT INTO "user" (name, deptid, orgid, email, password, usertype)  -- id = 5 / employee / dept = Limpeza
VALUES ('João', 6, 3, 'joao@4intelligence.com', '$argon2id$v=19$m=65536,t=3,p=4$0NMBnpJi+zMDOXbEQbinEA$CReTuQFvaMzh9+50m8Bs9n+nCNKbaPfS+2rvENkqbn8', 'employee');
INSERT INTO "user" (name, deptid, orgid, email, password, usertype)  -- id = 6 / employee / dept = Desenvolvimento
VALUES ('Marcos', 7, 3, 'marcos@4intelligence.com', '$argon2id$v=19$m=65536,t=3,p=4$0NMBnpJi+zMDOXbEQbinEA$CReTuQFvaMzh9+50m8Bs9n+nCNKbaPfS+2rvENkqbn8', 'employee');

/*
ADDING SURVEYS
*/
INSERT INTO "survey" (title, orgid) VALUES ('Pesquisa de satisfação', 1); -- id = 1
INSERT INTO "survey" (title, orgid) VALUES ('Pesquisa de clima de trabalho', 2); -- id = 2
INSERT INTO "survey" (title, orgid) VALUES ('Pesquisa de desenvolvimento de carreira', 2); -- id = 3
INSERT INTO "survey" (title, orgid) VALUES ('Pesquisa de satisfação', 3); -- id = 4

/*
ADDING QUESTIONS
*/
-- ORGANIZATION MY-KPI, SURVEY "Pesquisa de satisfação"
INSERT INTO "question" (title, scorefactor) VALUES ('Você se sente valorizado(a) pelo seu trabalho?', 2);       -- id = 1
INSERT INTO "question" (title, scorefactor) VALUES ('Como você avalia a comunicação interna da empresa?', 2);   -- id = 2
INSERT INTO "question" (title, scorefactor) VALUES ('O ambiente de trabalho promove o desenvolvimento profissional?', 2);   -- id = 3
INSERT INTO "question" (title, scorefactor) VALUES ('Você se sente motivado(a) a atingir suas metas profissionais?', 2);    -- id = 4
INSERT INTO "question" (title, scorefactor) VALUES ('Você acredita que tem oportunidades de crescimento na empresa?', 2);   -- id = 5
-- ORGANIZATION INATEL, SURVEY "Pesquisa de clima de trabalho"
INSERT INTO "question" (title, scorefactor) VALUES ('Como você avalia a qualidade das ferramentas de trabalho fornecidas pela empresa?', 2); -- id = 6
INSERT INTO "question" (title, scorefactor) VALUES ('Você está satisfeito(a) com o suporte técnico oferecido para resolver problemas com ferramentas e sistemas?', 2); -- id = 7
INSERT INTO "question" (title, scorefactor) VALUES ('O ambiente de trabalho é colaborativo e promove a troca de ideias?', 2);               -- id = 8
INSERT INTO "question" (title, scorefactor) VALUES ('Você sente que suas opiniões e sugestões são ouvidas pela equipe de gestão?', 2);      -- id = 9
INSERT INTO "question" (title, scorefactor) VALUES ('Você está satisfeito(a) com o equilíbrio entre sua vida pessoal e profissional?', 2);  -- id = 10
-- ORGANIZATION INATEL, SURVEY "Pesquisa de desenvolvimento de carreira"
INSERT INTO "question" (title, scorefactor) VALUES ('Você acredita que a empresa oferece oportunidades claras de crescimento na sua carreira?', 2);         -- id = 11
INSERT INTO "question" (title, scorefactor) VALUES ('Os planos de desenvolvimento de carreira são bem definidos e comunicados?', 2);                        -- id = 12
INSERT INTO "question" (title, scorefactor) VALUES ('Você se sente preparado(a) para alcançar seus objetivos de carreira com o suporte da empresa?', 2);    -- id = 13
INSERT INTO "question" (title, scorefactor) VALUES ('A empresa oferece treinamentos e capacitações suficientes para seu desenvolvimento profissional?', 2); -- id = 14
INSERT INTO "question" (title, scorefactor) VALUES ('Você sente que seu desempenho é avaliado de forma justa e que isso contribui para o seu crescimento na empresa?', 2); -- id = 15
-- ORGANIZATION 4INTELLIGENCE, SURVEY "Pesquisa de satisfação"
INSERT INTO "question" (title, scorefactor) VALUES ('Como você avalia a clareza das metas e objetivos do seu trabalho?', 2);                                -- id = 16
INSERT INTO "question" (title, scorefactor) VALUES ('Você está satisfeito(a) com as oportunidades de crescimento e desenvolvimento dentro da empresa?', 2); -- id = 17
INSERT INTO "question" (title, scorefactor) VALUES ('A comunicação interna da empresa é eficiente e transparente?', 2);                                     -- id = 18
INSERT INTO "question" (title, scorefactor) VALUES ('Você está satisfeito(a) com o suporte oferecido para seu desenvolvimento profissional (cursos, treinamentos, certificações)?', 2); -- id = 19
INSERT INTO "question" (title, scorefactor) VALUES ('Você recomendaria esta empresa a outros profissionais da área de tecnologia?', 2);                     -- id = 20

/*
BIND SURVEY AND QUESTIONS
*/
-- ORGANIZATION MY-KPI, SURVEY "Pesquisa de satisfação"
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (1, 1);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (1, 2);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (1, 3);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (1, 4);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (1, 5);
-- ORGANIZATION INATEL, SURVEY "Pesquisa de clima de trabalho"
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (2, 6);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (2, 7);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (2, 8);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (2, 9);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (2, 10);
-- ORGANIZATION INATEL, SURVEY "Pesquisa de desenvolvimento de carreira"
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (3, 11);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (3, 12);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (3, 13);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (3, 14);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (3, 15);
-- ORGANIZATION 4INTELLIGENCE, SURVEY "Pesquisa de satisfação"
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (4, 16);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (4, 17);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (4, 18);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (4, 19);
INSERT INTO "surveyquestions" (surveyid, questionid) VALUES (4, 20);

/*
INSERT ANSWERS
*/
-- ORGANIZATION INATEL, SURVEY "Pesquisa de clima de trabalho", USER Pedro
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 6, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 7, 5);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 8, 3);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 9, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 10, 5);
-- ORGANIZATION INATEL, SURVEY "Pesquisa de desenvolvimento de carreira", USER Pedro
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 11, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 12, 5);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 13, 3);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 14, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (3, 15, 5);
-- ORGANIZATION 4INTELLIGENCE, SURVEY "Pesquisa de satisfação", USER João
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (5, 16, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (5, 17, 5);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (5, 18, 3);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (5, 19, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (5, 20, 5);
-- ORGANIZATION 4INTELLIGENCE, SURVEY "Pesquisa de satisfação", USER Marcos
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (6, 16, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (6, 17, 5);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (6, 18, 3);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (6, 19, 4);
INSERT INTO "questionscore" (employeeid, questionid, score) VALUES (6, 20, 5);