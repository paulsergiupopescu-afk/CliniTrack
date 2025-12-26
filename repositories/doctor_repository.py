from repositories.repository_interface import RepositoryInterface
from database.connection import get_cursor_and_connection
from models.doctor import Doctor


class DoctorRepository(RepositoryInterface):
    def __init__(self):
        pass

    def create(self, data):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       INSERT INTO doctors
                           (doctor_id, doctor_name, speciality, room, is_active)
                       VALUES (?, ?, ?, ?, ?)
                       ''', (data['doctor_id'], data['name'], data['speciality'],
                             data['room'], data['is_active']))

        conn.commit()
        return data['doctor_id']

    def read(self, doctor_id):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       SELECT *
                       FROM doctors
                       WHERE doctor_id = ?
                       ''', (doctor_id,))

        row = cursor.fetchone()

        if row:
            return Doctor(row[0], row[1], row[2], row[3], row[4])

        return None

    def update(self, doctor_id, data):
        cursor, conn = get_cursor_and_connection()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return False

        values.append(doctor_id)
        query = f"UPDATE doctors SET {', '.join(fields)} WHERE doctor_id = ?"
        cursor.execute(query, values)
        conn.commit()

        return cursor.rowcount > 0

    def delete(self, doctor_id):
        cursor, conn = get_cursor_and_connection()
        cursor.execute('DELETE FROM doctors WHERE doctor_id = ?', (doctor_id,))
        conn.commit()
        return cursor.rowcount > 0