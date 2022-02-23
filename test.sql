SELECT job_id, company_details.company_name, location, 
title, description, job_type, prerequisites, skills, 
pay_rate, no_positions, experience_required 
FROM (select * from job_details where status = '1' limit 10 offset 0) as jobs
join company_details on
company_details.company_id = jobs.company_id;