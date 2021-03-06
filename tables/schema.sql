CREATE table IF NOT EXISTS company_details(
    company_id SERIAL PRIMARY KEY,
    company_name text,
    location text,
    department text,
    about_us text, 
    rating smallint,
    awards text,
    contact char(10),
    email text,
    website text
); 

CREATE INDEX company_index ON company_details
(
    company_name ASC
);

CREATE INDEX location_index ON company_details
(
    location ASC
);

CREATE table IF NOT EXISTS job_details(
    job_id SERIAL PRIMARY KEY,
    company_id bigint REFERENCES company_details(company_id),
    title text,
    description text,
    job_type text,
    prerequisites text,
    skills text,
    pay_rate text,
    no_positions FLOAT,
    experience_required text,
    status bit
); 

CREATE INDEX job_skills ON job_details
(
    skills ASC
);

CREATE INDEX job_index ON job_details
(
    title ASC
);

CREATE TABLE IF NOT EXISTS user_details(
    user_id SERIAL PRIMARY KEY,
    firstname text,
    lastname text,
    age bigint,
    gender text,
    ethnicity text,
    address text,
    state text,
    email text,
    contact text,
    Education text
);


CREATE TABLE IF NOT EXISTS experiences(
    exp_id SERIAL PRIMARY KEY,
    company text,
    start_year bigint,
    years bigint,
    role text,
    user_id bigint REFERENCES user_details(user_id)
);

CREATE INDEX experience_index ON experiences
(
    user_id ASC
);


CREATE TABLE IF NOT EXISTS applications(
    application_id SERIAL PRIMARY KEY,
    job_id bigint REFERENCES job_details(job_id) on delete cascade,
    user_id bigint REFERENCES user_details(user_id),
    status smallint
);

CREATE INDEX application_index ON applications
(
    job_id ASC
);

CREATE TABLE IF NOT EXISTS login_details(
    pid SERIAL PRIMARY KEY,
    login_id text unique,
    password text,
    userorcompany text,
    user_id bigint REFERENCES user_details(user_id),
    company_id bigint REFERENCES company_details(company_id)
);


CREATE OR REPLACE FUNCTION user_trig ()
RETURNS trigger AS
$$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM experiences WHERE user_id = OLD.user_id;
            DELETE FROM applications WHERE user_id = OLD.user_id;
            DELETE FROM login_details WHERE user_id = OLD.user_id;
        END IF;
        RETURN OLD;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER user_trigger BEFORE DELETE ON user_details
FOR EACH ROW
EXECUTE PROCEDURE user_trig();

CREATE OR REPLACE FUNCTION company_trig ()
RETURNS trigger AS
$$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM job_details WHERE company_id = OLD.company_id;
            DELETE FROM applications WHERE company_id = OLD.company_id;
            DELETE FROM login_details WHERE company_id = OLD.company_id;
        END IF;
        RETURN OLD;
    END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER company_trigger BEFORE DELETE ON company_details
FOR EACH ROW
EXECUTE PROCEDURE company_trig();


\copy company_details from 'tables/company_details.csv' DELIMITER ',' CSV HEADER;
\copy job_details from 'tables/job_details.csv' DELIMITER ',' CSV HEADER;
\copy user_details from 'tables/userDetails.csv' DELIMITER ',' CSV HEADER;
\copy experiences from 'tables/experiences.csv' DELIMITER ',' CSV HEADER;
\copy login_details from 'tables/login_details.csv' DELIMITER ',' NULL AS '' CSV HEADER ;
\copy applications from 'tables/applications.csv' DELIMITER ',' CSV HEADER;

-- \copy company_details from 'C:\\Users\\gupta\\Sem6\\COL362_DBMS\\project\\COL362-DBMS-Project\\tables\\company_details.csv' DELIMITER ',' CSV HEADER;
-- \copy job_details from 'C:\\Users\\gupta\\Sem6\\COL362_DBMS\\project\\COL362-DBMS-Project\\tables\\job_details.csv' DELIMITER ',' CSV HEADER;
-- \copy user_details from 'C:\\Users\\gupta\\Sem6\\COL362_DBMS\\project\\COL362-DBMS-Project\\tables\\userDetails.csv' DELIMITER ',' CSV HEADER;
-- \copy experiences from 'C:\\Users\\gupta\\Sem6\\COL362_DBMS\\project\\COL362-DBMS-Project\\tables\\experiences.csv' DELIMITER ',' CSV HEADER;
-- \copy login_details from 'C:\\Users\\gupta\\Sem6\\COL362_DBMS\\project\\COL362-DBMS-Project\\tables\\login_details.csv' DELIMITER ',' NULL AS '' CSV HEADER ;
-- \copy applications from 'C:\\Users\\gupta\\Sem6\\COL362_DBMS\\project\\COL362-DBMS-Project\\tables\\applications.csv' DELIMITER ',' CSV HEADER;


