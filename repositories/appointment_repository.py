from repositories.repository_interface import RepositoryInterface
from database.connection import get_cursor_and_connection
from models.appointment import Appointment


class AppointmentRepository(RepositoryInterface):
    def __init__(self):
        pass

    def create(self, data):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       INSERT INTO appointments
                       (patient_id, doctor_id, date, start_time, end_time, status,
                        source, procedure_name, procedure_category, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                       ''', (data['patient_id'], data['doctor_id'], data['date'],
                             data['start_time'], data['end_time'], data.get('status', 'Confirmed'),
                             data.get('source', 'Online'), data['procedure_name'],
                             data['procedure_category']))

        conn.commit()
        return cursor.lastrowid

    def read(self, appointment_id):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       SELECT *
                       FROM appointments
                       WHERE id = ?
                       ''', (appointment_id,))

        row = cursor.fetchone()

        if row:
            return Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8])

        return None

    def update(self, appointment_id, data):
        cursor, conn = get_cursor_and_connection()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return False

        values.append(appointment_id)
        query = f"UPDATE appointments SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()

        return cursor.rowcount > 0

    def delete(self, appointment_id):
        cursor, conn = get_cursor_and_connection()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        conn.commit()
        return cursor.rowcount > 0