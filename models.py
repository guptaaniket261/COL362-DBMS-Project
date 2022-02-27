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