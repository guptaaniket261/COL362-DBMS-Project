-- CREATE table IF NOT EXISTS company_details(
--     company_id SERIAL PRIMARY KEY,
--     company_name text,
--     location text,
--     department text,
--     about_us text, 
--     rating smallint,
--     awards text,
--     contact char(10),
--     email text,
--     website text
-- ); 

-- CREATE table IF NOT EXISTS job_details(
--     job_id SERIAL PRIMARY KEY,
--     company_id bigint REFERENCES company_details(company_id),
--     title text,
--     description text,
--     job_type text,
--     prerequisites text,
--     skills text,
--     pay_rate text,
--     no_positions FLOAT,
--     experience_required text,
--     status bit
-- ); 


-- CREATE TABLE IF NOT EXISTS user_details(
--     user_id SERIAL PRIMARY KEY,
--     firstname text,
--     lastname text,
--     age bigint,
--     gender text,
--     ethnicity text,
--     address text,
--     state text,
--     email text,
--     contact text,
--     Education text
-- );

--  CREATE TABLE IF NOT EXISTS experiences(
--     exp_id SERIAL PRIMARY KEY,
--     start_year bigint,
--     years bigint,
--     role text,
--     user_id bigint REFERENCES user_details(user_id)

-- );


CREATE TABLE IF NOT EXISTS experiences(
    exp_id SERIAL PRIMARY KEY,
    company text,
    start_year bigint,
    years bigint,
    role text,
    user_id bigint REFERENCES user_details(user_id)
);


-- CREATE TABLE IF NOT EXISTS applications(
--     application_id SERIAL PRIMARY KEY,
--     job_id bigint REFERENCES job_details(job_id),
--     user_id bigint REFERENCES user_details(user_id),
--     status smallint
-- );


-- CREATE TABLE IF NOT EXISTS login_details(
--     pid SERIAL PRIMARY KEY,
--     login_id text unique,
--     password text,
--     userorcompany text,
--     user_id bigint REFERENCES user_details(user_id),
--     company_id bigint REFERENCES company_details(company_id)
-- );

-- \copy company_details from 'company_details_latest.csv' DELIMITER ',' CSV HEADER;
-- \copy job_details from 'job_details.csv' DELIMITER ',' CSV HEADER;
-- \copy user_details from 'userDetailsLatest.csv' DELIMITER ',' CSV HEADER;
-- \copy experiences from 'experiencesNew.csv' DELIMITER ',' CSV HEADER;
\copy login_details from 'login_details.csv' DELIMITER ',' NULL AS 'null' CSV HEADER ;

