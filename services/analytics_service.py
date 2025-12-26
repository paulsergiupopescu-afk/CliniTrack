import sqlite3
from datetime import datetime


class AnalyticsService:
    # handles analytics for the dental clinic
    # probably not the most efficient way but it works

    def __init__(self, db_path="database/dentalclinic.db"):
        self.db_path = db_path

    def get_connection(self):
        # get database connection
        return sqlite3.connect(self.db_path)

    def get_patient_demographics(self):
        # get patient stats - age groups and gender distribution
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT patient_birthdate, gender FROM patients")
        patients = cursor.fetchall()
        conn.close()

        if not patients:
            return None

        # count age groups manually - easier to understand than fancy libraries
        age_groups = {'0-17': 0, '18-29': 0, '30-44': 0, '45-59': 0, '60+': 0}
        gender_count = {'M': 0, 'F': 0}

        for patient in patients:
            birthdate = patient[0]
            gender = patient[1]

            # calculate age
            try:
                birth = datetime.strptime(birthdate, '%Y-%m-%d')
                age = datetime.now().year - birth.year

                # put in right age group
                if age < 18:
                    age_groups['0-17'] += 1
                elif age < 30:
                    age_groups['18-29'] += 1
                elif age < 45:
                    age_groups['30-44'] += 1
                elif age < 60:
                    age_groups['45-59'] += 1
                else:
                    age_groups['60+'] += 1

                # count gender
                if gender in gender_count:
                    gender_count[gender] += 1
            except:
                # skip if date is weird
                pass

        return {
            'total_patients': len(patients),
            'age_groups': age_groups,
            'gender': gender_count
        }

    def get_appointment_trends(self):
        # get appointment trends - monthly breakdown and status
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT date, status, procedure_category FROM appointments ORDER BY date")
        appointments = cursor.fetchall()
        conn.close()

        if not appointments:
            return None

        # track monthly appointments
        # TODO: maybe use pandas for this? seems like it would be faster
        monthly_data = {}
        status_count = {}
        category_count = {}

        for appt in appointments:
            date = appt[0]
            status = appt[1]
            category = appt[2]

            # get month/year from date
            month_year = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')

            # initialize month if not exists
            if month_year not in monthly_data:
                monthly_data[month_year] = {'total': 0, 'completed': 0, 'cancelled': 0}

            # count totals
            monthly_data[month_year]['total'] += 1
            if status == 'Completed':
                monthly_data[month_year]['completed'] += 1
            elif status == 'Cancelled':
                monthly_data[month_year]['cancelled'] += 1

            # count status
            if status not in status_count:
                status_count[status] = 0
            status_count[status] += 1

            # count categories
            if category:
                if category not in category_count:
                    category_count[category] = 0
                category_count[category] += 1

        return {
            'total_appointments': len(appointments),
            'monthly_trends': monthly_data,
            'status_distribution': status_count,
            'category_distribution': category_count
        }

    def get_peak_hours_analysis(self):
        # find out when clinic is busiest - hours and days
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT start_time, date FROM appointments WHERE status = 'Completed'")
        appointments = cursor.fetchall()
        conn.close()

        if not appointments:
            return None

        # count by hour and weekday
        hour_count = {}
        weekday_count = {}

        for appt in appointments:
            start_time = appt[0]
            date = appt[1]

            # get hour from start time
            hour = int(start_time.split(':')[0])
            if hour not in hour_count:
                hour_count[hour] = 0
            hour_count[hour] += 1

            # get weekday name
            weekday = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
            if weekday not in weekday_count:
                weekday_count[weekday] = 0
            weekday_count[weekday] += 1

        # find peak hour and busiest day
        # not the cleanest code but works
        peak_hour = None
        max_hour_count = 0
        for hour, count in hour_count.items():
            if count > max_hour_count:
                max_hour_count = count
                peak_hour = (hour, count)

        busiest_day = None
        max_day_count = 0
        for day, count in weekday_count.items():
            if count > max_day_count:
                max_day_count = count
                busiest_day = (day, count)

        return {
            'hourly_distribution': dict(sorted(hour_count.items())),
            'weekday_distribution': weekday_count,
            'peak_hour': peak_hour,
            'busiest_day': busiest_day
        }

    def get_revenue_analysis(self):
        # calculate total revenue and breakdown by procedure
        conn = self.get_connection()
        cursor = conn.cursor()

        # get payments with appointment info
        cursor.execute("""
            SELECT p.amount, p.method, a.procedure_name, a.date
            FROM payments p
            JOIN appointments a ON p.appointment_id = a.id
        """)
        payments = cursor.fetchall()
        conn.close()

        if not payments:
            return None

        total_revenue = 0
        monthly_revenue = {}
        payment_methods = {}
        procedure_revenue = {}

        for payment in payments:
            amount = payment[0]
            method = payment[1]
            procedure = payment[2]
            date = payment[3]

            # add to total
            total_revenue += amount

            # track by month
            month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
            if month not in monthly_revenue:
                monthly_revenue[month] = 0
            monthly_revenue[month] += amount

            # count payment methods
            if method not in payment_methods:
                payment_methods[method] = 0
            payment_methods[method] += 1

            # track revenue by procedure
            if procedure not in procedure_revenue:
                procedure_revenue[procedure] = 0
            procedure_revenue[procedure] += amount

        # get top 5 procedures by revenue
        # sort by revenue descending
        sorted_procedures = sorted(procedure_revenue.items(), key=lambda x: x[1], reverse=True)
        top_procedures = [(proc, round(rev, 2)) for proc, rev in sorted_procedures[:5]]

        avg_payment = total_revenue / len(payments) if payments else 0

        return {
            'total_revenue': round(total_revenue, 2),
            'average_payment': round(avg_payment, 2),
            'monthly_revenue': {k: round(v, 2) for k, v in sorted(monthly_revenue.items())},
            'payment_methods': payment_methods,
            'top_procedures': top_procedures
        }

    def get_doctor_performance(self):
        # get stats for each doctor - appointments and completion rates
        # doing this with simple queries - probably not optimal but easier to understand
        conn = self.get_connection()
        cursor = conn.cursor()

        # get all active doctors
        cursor.execute("SELECT doctor_id, doctor_name, speciality FROM doctors WHERE is_active = 1")
        doctors = cursor.fetchall()

        performance = []

        for doctor in doctors:
            doctor_id = doctor[0]
            doctor_name = doctor[1]
            specialty = doctor[2]

            # get all appointments for this doctor
            cursor.execute("SELECT status FROM appointments WHERE doctor_id = ?", (doctor_id,))
            appointments = cursor.fetchall()

            # count completed vs total
            total = len(appointments)
            completed = 0
            cancelled = 0

            for appt in appointments:
                if appt[0] == 'Completed':
                    completed += 1
                elif appt[0] == 'Cancelled':
                    cancelled += 1

            # calculate completion rate
            if total > 0:
                completion_rate = (completed / total) * 100
            else:
                completion_rate = 0

            performance.append({
                'name': doctor_name,
                'specialty': specialty,
                'total_appointments': total,
                'completed': completed,
                'cancelled': cancelled,
                'completion_rate': round(completion_rate, 1)
            })

        conn.close()
        return performance

    def get_dashboard_summary(self):
        # get everything for the dashboard
        # just calls all the other methods
        demographics = self.get_patient_demographics()
        appointments = self.get_appointment_trends()
        peak_hours = self.get_peak_hours_analysis()
        revenue = self.get_revenue_analysis()
        doctors = self.get_doctor_performance()

        return {
            'demographics': demographics,
            'appointments': appointments,
            'peak_hours': peak_hours,
            'revenue': revenue,
            'doctor_performance': doctors
        }
