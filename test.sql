Select * from login_details where login_id='aarti1@gmail.com' and password='670656';

-- insert into user_details values (2001, 'Aniket', 'Gupta', 21, 'Male', 'Indian', 'UP', 'UP', 'guptaaniket261@gmail.com', '1234567890', 'CBSE');

SELECT job_id, company_details.company_name, location, 
                  title, description, job_type, prerequisites, skills, 
                  pay_rate, no_positions, experience_required 
                  FROM (select * from job_details where status = '1' limit 10 offset 0) as jobs
                  join company_details on
                  company_details.company_id = jobs.company_id and
                  job_id not in (select job_id from applications where user_id=2001);


SELECT * FROM applications WHERE user_id = 2001;

SELECT application_id, firstname, lastname, age, gender, education, email, contact, status, user_id FROM 
  (user_details NATURAL JOIN (SELECT * FROM applications WHERE  job_id = 1) b) a ORDER BY application_id;

DELETE FROM job_details WHERE job_id = 100;

SELECT jobs.job_id, company_details.company_name,  
                    title, description, job_type, prerequisites, skills, 
                    pay_rate, no_positions, experience_required , location, 
                    contact, email, applications.status
                    FROM job_details as jobs
                    join company_details on
                    company_details.company_id = jobs.company_id 
                    join applications on
                    applications.job_id = jobs.job_id 
                    and applications.user_id = 2001;

UPDATE company_details SET company_name = 'Airtel', about_us = '-', department = 'Telecom', location = 'Delhi', awards = 'none', contact = '1234567890', website = 'airtel.com' WHERE company_id = 1000;

