class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, date, start_time, end_time,
                 status, procedure_name, source=None, procedure_category=None,
                 created_at=None, notes=None):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.procedure_name = procedure_name
        self.source = source
        self.procedure_category = procedure_category
        self.created_at = created_at
        self.notes = notes

    def __repr__(self):
        return f"Appointment(id={self.appointment_id}, date='{self.date}', status='{self.status}')"

    def is_completed(self):
        # check if appointment is completed
        return self.status == 'Completed'

    def is_future(self):
        # check if appointment is in the future
        from datetime import datetime
        appointment_date = datetime.strptime(self.date, '%Y-%m-%d').date()
        return appointment_date > datetime.now().date()

    def get_duration_minutes(self):
        # calculate appointment duration in minutes
        from datetime import datetime
        start = datetime.strptime(self.start_time, '%H:%M')
        end = datetime.strptime(self.end_time, '%H:%M')
        duration = (end - start).seconds // 60
        return duration