class Doctor:
    def __init__(self, doctor_id, doctor_name, speciality, room, is_active,
                 education=None, experience_years=None, work_days=None, phone=None, email=None):
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.speciality = speciality
        self.room = room
        self.is_active = is_active
        self.education = education
        self.experience_years = experience_years
        self.work_days = work_days
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Doctor(id={self.doctor_id}, name='{self.doctor_name}', speciality='{self.speciality}')"

    def is_available(self):
        # check if doctor is currently active
        return self.is_active == 1