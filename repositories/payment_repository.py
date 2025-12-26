from repositories.repository_interface import RepositoryInterface
from database.connection import get_cursor_and_connection
from models.payment import Payment


class PaymentRepository(RepositoryInterface):
    def __init__(self):
        pass

    def create(self, data):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       INSERT INTO payments
                           (appointment_id, amount, method, paid_at)
                       VALUES (?, ?, ?, datetime('now'))
                       ''', (data['appointment_id'], data['amount'], data.get('method', 'Cash')))

        conn.commit()
        return cursor.lastrowid

    def read(self, payment_id):
        cursor, conn = get_cursor_and_connection()

        cursor.execute('''
                       SELECT *
                       FROM payments
                       WHERE id = ?
                       ''', (payment_id,))

        row = cursor.fetchone()

        if row:
            return Payment(row[0], row[1], row[2], row[3], row[4])

        return None

    def update(self, payment_id, data):
        cursor, conn = get_cursor_and_connection()

        fields = []
        values = []

        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if not fields:
            return False

        values.append(payment_id)
        query = f"UPDATE payments SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()

        return cursor.rowcount > 0

    def delete(self, payment_id):
        cursor, conn = get_cursor_and_connection()
        cursor.execute('DELETE FROM payments WHERE id = ?', (payment_id,))
        conn.commit()
        return cursor.rowcount > 0