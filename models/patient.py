class Patient:
    def __init__(self, patient_id, patient_name, patient_birthdate, first_visit_at,
                 gender, city, address=None, phone=None, email=None, insurance=None):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.patient_birthdate = patient_birthdate
        self.first_visit_at = first_visit_at
        self.gender = gender
        self.city = city
        self.address = address
        self.phone = phone
        self.email = email
        self.insurance = insurance

    def __repr__(self):
        return f"Patient(id={self.patient_id}, name='{self.patient_name}', city='{self.city}')"

    def get_age(self):
        # calculates patient age from birthdate
        from datetime import datetime
        birthdate = datetime.strptime(self.patient_birthdate, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birthdate.year
        # adjust if birthday hasn't happened this year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        return age

    def has_insurance(self):
        # check if patient has insurance coverage
        return self.insurance and self.insurance != 'None'