SELECT * FROM experiences WHERE user_id IN 
(SELECT user_id FROM applications WHERE job_id = 4 );