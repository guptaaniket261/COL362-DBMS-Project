
/*
CREATE table IF NOT EXISTS company_details(
    company_id bigint PRIMARY KEY,
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
\copy company_details from tables/company_details.csv DELIMITER ',' CSV HEADER;

CREATE table IF NOT EXISTS job_details(
    job_id bigint PRIMARY KEY,
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

\copy job_details from tables/job_details.csv DELIMITER ',' CSV HEADER;
*/

CREATE TABLE IF NOT EXISTS user_details(
    user_id bigint PRIMARY KEY,
    firstname text,
    lastname text,
    age smallint,
    gender CHAR(1),
    ethnicity text,
    address text,
    /*experiences*/  
    email text,
    contact char(10)
);
CREATE TABLE IF NOT EXISTS applications(
    application_id bigint PRIMARY KEY,
    job_id bigint REFERENCES job_details(job_id),
    user_id bigint REFERENCES user_details(user_id),
    status smallint
);

INSERT INTO user_details(user_id, firstname, lastname, contact) VALUES(1, 'Hello', 'World', '0000000000');
INSERT INTO applications VALUES(1,16349, 1, 1);