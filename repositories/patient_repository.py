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
            # Handle both old schema (6 columns) and new schema (10 columns)
            if len(row) >= 10:
                # New schema with all fields
                return Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                              row[6], row[7], row[8], row[9])
            else:
                # Old schema - provide defaults for missing fields
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
        """Returneaza toti pacientii"""
        cursor, conn = get_cursor_and_connection()

        cursor.execute('SELECT * FROM patients ORDER BY patient_id')
        rows = cursor.fetchall()

        patients = []
        for row in rows:
            # Handle both old schema (6 columns) and new schema (10 columns)
            if len(row) >= 10:
                # New schema with all fields
                patients.append(Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                                      row[6], row[7], row[8], row[9]))
            else:
                # Old schema - provide defaults for missing fields
                patients.append(Patient(row[0], row[1], row[2], row[3], row[4], row[5],
                                      None, None, None, None))

        return patients