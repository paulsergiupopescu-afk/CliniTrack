from repositories.repository_interface import RepositoryInterface
from database.connection import get_cursor_and_connection
from models.patient import Patient


class PatientRepository(RepositoryInterface):
    def __init__(self):
        pass

    def create(self, data):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       INSERT INTO patients
                           (patient_name, patient_birthdate, first_visit_at, gender, city)
                       VALUES (?, ?, ?, ?, ?)
                       ''', (data['name'], data['birthdate'], data['first_visit'],
                             data['gender'], data['city']))

        conn.commit()
        return cursor.lastrowid

    def read(self, patient_id):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       SELECT *
                       FROM patients
                       WHERE patient_id = ?
                       ''', (patient_id,))

        row = cursor.fetchone()

        if row:
            # support different database column counts for backwards compatibility
            if len(row) >= 10:
                return Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                              row[6], row[7], row[8], row[9])
            else:
                return Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                              None, None, None, None)

        return None

    def update(self, patient_id, data):
        cursor, conn = get_cursor_and_connection()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return False

        values.append(patient_id)
        query = f"UPDATE patients SET {', '.join(fields)} WHERE patient_id = ?"
        cursor.execute(query, values)
        conn.commit()

        return cursor.rowcount > 0

    def delete(self, patient_id):
        cursor, conn = get_cursor_and_connection()
        cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
        conn.commit()
        return cursor.rowcount > 0

    def get_all(self):
        # returns all patients from database
        cursor, conn = get_cursor_and_connection()

        cursor.execute('SELECT * FROM patients ORDER BY patient_id')
        rows = cursor.fetchall()

        patients = []
        for row in rows:
            if len(row) >= 10:
                patients.append(Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                                      row[6], row[7], row[8], row[9]))
            else:
                patients.append(Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                                      None, None, None, None))

        return patients

    def search_by_name(self, name):
        # search patients by name - just a simple text match
        cursor, conn = get_cursor_and_connection()

        # using LIKE to find partial matches
        search_term = f"%{name}%"
        cursor.execute('SELECT * FROM patients WHERE patient_name LIKE ? ORDER BY patient_name', (search_term,))
        rows = cursor.fetchall()

        patients = []
        for row in rows:
            if len(row) >= 10:
                patients.append(Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                                      row[6], row[7], row[8], row[9]))
            else:
                patients.append(Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                                      None, None, None, None))

        return patients