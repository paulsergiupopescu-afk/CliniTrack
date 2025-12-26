class Payment:
    def __init__(self, payment_id, appointment_id, amount, method, paid_at, status='Completed'):
        self.payment_id = payment_id
        self.appointment_id = appointment_id
        self.amount = amount
        self.method = method
        self.paid_at = paid_at
        self.status = status

    def __repr__(self):
        return f"Payment(id={self.payment_id}, amount={self.amount}, method='{self.method}', status='{self.status}')"

    def is_completed(self):
        """Check if payment is completed"""
        return self.status == 'Completed'

    def is_pending(self):
        """Check if payment is pending"""
        return self.status == 'Pending'

    def get_formatted_amount(self):
        """Get formatted amount in RON"""
        return f"{self.amount:.2f} RON"