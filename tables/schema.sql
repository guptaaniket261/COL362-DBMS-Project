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




 CREATE TABLE IF NOT EXISTS user_details(
     user_id bigint PRIMARY KEY,
     firstname text,
     lastname text,
     age smallint,
     gender CHAR(1),
     ethnicity text,
     address text,
     state text,
     email text,
     contact char(10),
     Education text
 );

 CREATE TABLE IF NOT EXISTS experiences(
    exp_id bigint PRIMARY KEY,
    company text,
    start_year bigint,
    years bigint,
    role text,
    user_id bigint REFERENCES user_details(user_id)

);

\copy company_details from tables/company_details.csv DELIMITER ',' CSV HEADER;
\copy job_details from tables/job_details.csv DELIMITER ',' CSV HEADER;
\copy user_details from tables/userDetailsNew.csv DELIMITER ',' CSV HEADER;
\copy experiences from tables/experiencesNew.csv DELIMITER ',' CSV HEADER;