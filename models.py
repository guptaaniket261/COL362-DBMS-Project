class UserDetails:
  def __init__(self):
    self.user_id = -1
    

  def __init__(self, user_id, firstname, lastname, age, gender, ethnicity, address, state, email, contact, education):
    self.user_id = user_id
    self.firstname = firstname
    self.lastname = lastname
    self.age = age
    self.gender = gender
    self.ethnicity = ethnicity
    self.address = address
    self.state = state
    self.email = email
    self.contact = contact
    self.education = education


class JobDetail:
  def __init__(self, job_id, company, job_title, description, job_type, prerequisites, skills, pay_rate, no_positions, experience_required, location, contact, email, status = "APPLICATION IN PROCESS"):
    self.job_id = job_id
    self.company = company
    self.job_title = job_title
    self.description = description
    self.job_type = job_type
    self.prerequisites = prerequisites
    self.skills = skills
    self.pay_rate = pay_rate
    self.no_positions = no_positions
    self.experience_required = experience_required
    self.location = location
    self.contact = contact
    self.email = email
    self.status = status



    
    