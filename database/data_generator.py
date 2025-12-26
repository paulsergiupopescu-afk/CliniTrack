import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta, time
import os

# Configure for Romania
fake = Faker('ro_RO')

# Database path configuration
PATH_DB = "database/dentalclinic.db"


class BucharestDentalClinicGenerator:
    def __init__(self):
        self.conn = sqlite3.connect(PATH_DB)
        self.cursor = self.conn.cursor()

        # Realistic Bucharest data
        self.SECTORS = [
            'Sector 1', 'Sector 2', 'Sector 3', 'Sector 4',
            'Sector 5', 'Sector 6', 'Old Town', 'Herastrau',
            'Floreasca', 'Calea Victoriei', 'Amzei', 'Dorobanti'
        ]

        # Bucharest neighborhoods and areas
        self.NEIGHBORHOODS = [
            'Herastrau', 'Floreasca', 'Primaverii', 'Dorobanti', 'Aviatorilor',
            'Calea Victoriei', 'Amzei', 'Piata Romana', 'Universitate',
            'Vitan', 'Dristor', 'Colentina', 'Pantelimon', 'Titan',
            'Drumul Taberei', 'Militari', 'Grozavesti', 'Politehnica'
        ]

        # Realistic doctors with specializations
        self.DOCTORS = [
            ("Dr. Elena Popescu", "General Dentistry", "University of Medicine Bucharest", 15),
            ("Dr. Andrei Ionescu", "Orthodontics", "University of Medicine Cluj", 12),
            ("Dr. Maria Constantinescu", "Endodontics", "University of Medicine Bucharest", 18),
            ("Dr. Mihai Georgescu", "Oral Surgery", "University of Medicine Iasi", 20),
            ("Dr. Ana Dumitrescu", "Periodontics", "University of Medicine Bucharest", 14),
            ("Dr. Cristian Radu", "Implantology", "University of Medicine Timisoara", 16),
            ("Dr. Ioana Vasilescu", "Prosthodontics", "University of Medicine Bucharest", 13),
            ("Dr. Alexandru Stan", "Pediatric Dentistry", "University of Medicine Cluj", 10),
            ("Dr. Carmen Stoica", "Aesthetic Dentistry", "University of Medicine Bucharest", 11),
            ("Dr. Gabriel Nistor", "General Dentistry", "University of Medicine Iasi", 8)
        ]

        # Procedures with realistic 2024-2025 prices in RON
        self.PROCEDURES = [
            ('Consultation', 'Diagnostic', 30, 150, 200),
            ('Intraoral X-Ray', 'Diagnostic', 15, 80, 120),
            ('Panoramic X-Ray', 'Diagnostic', 20, 150, 200),
            ('Scaling', 'Hygiene', 60, 250, 350),
            ('Professional Cleaning', 'Hygiene', 30, 150, 200),
            ('Composite Filling', 'Treatment', 45, 300, 500),
            ('Amalgam Filling', 'Treatment', 30, 200, 300),
            ('Root Canal Molar', 'Endodontics', 120, 800, 1200),
            ('Root Canal Premolar', 'Endodontics', 90, 600, 900),
            ('Root Canal Incisor', 'Endodontics', 60, 400, 600),
            ('Simple Extraction', 'Surgery', 30, 200, 300),
            ('Surgical Extraction', 'Surgery', 60, 400, 600),
            ('Wisdom Tooth Extraction', 'Surgery', 90, 600, 1000),
            ('Ceramic Crown', 'Prosthetics', 60, 1500, 2500),
            ('Zirconia Crown', 'Prosthetics', 60, 2000, 3500),
            ('3-Unit Bridge', 'Prosthetics', 120, 4000, 6500),
            ('Dental Implant', 'Implantology', 90, 3500, 5500),
            ('Implant + Crown', 'Implantology', 120, 5500, 8500),
            ('Metal Braces', 'Orthodontics', 45, 3000, 4500),
            ('Ceramic Braces', 'Orthodontics', 45, 4500, 6500),
            ('Invisalign', 'Orthodontics', 30, 8000, 15000),
            ('Teeth Whitening', 'Aesthetics', 90, 800, 1500),
            ('Veneer Composite', 'Aesthetics', 60, 600, 1200),
            ('Veneer Porcelain', 'Aesthetics', 90, 2000, 3500),
            ('Gum Treatment', 'Periodontics', 45, 300, 600),
            ('Bone Graft', 'Surgery', 120, 1500, 3000)
        ]

        # Insurance companies in Romania
        self.INSURANCE = [
            'CNAS', 'Regina Maria', 'Medicover', 'MedLife', 'Sanador',
            'Policlinica de Diagnostic Rapid', 'None'
        ]

        # Phone prefixes for Bucharest
        self.PHONE_PREFIXES = ['021', '031', '0722', '0723', '0724', '0725', '0726', '0727', '0728', '0729']

    def generate_realistic_phone(self):
        """Generate realistic Romanian phone number"""
        prefix = random.choice(self.PHONE_PREFIXES)
        if prefix.startswith('02') or prefix.startswith('03'):
            # Landline
            return f"{prefix}.{random.randint(100, 999)}.{random.randint(100, 999)}"
        else:
            # Mobile
            return f"{prefix}.{random.randint(100, 999)}.{random.randint(100, 999)}"

    def generate_realistic_address(self):
        """Generate realistic Bucharest address"""
        street_types = ['Str.', 'Bd.', 'Calea', 'Aleea', 'Piata']
        street_names = [
            'Mihai Eminescu', 'Ion Creanga', 'Nicolae Iorga', 'Octavian Goga',
            'Mircea Eliade', 'George Enescu', 'Nicolae Grigorescu', 'Stefan Luchian',
            'Republicii', 'Libertății', 'Unirii', 'Victoriei', 'Pacii', 'Florilor'
        ]

        street_type = random.choice(street_types)
        street_name = random.choice(street_names)
        number = random.randint(1, 200)
        sector = random.choice(self.SECTORS)

        return f"{street_type} {street_name} {number}, {sector}, Bucharest"

    def clear_existing_data(self):
        """Clear existing data from tables"""
        tables = ['payments', 'appointments', 'procedures', 'doctors', 'patients']
        for table in tables:
            self.cursor.execute(f'DELETE FROM {table}')
        print("Existing data cleared.")

    def generate_patients(self, count=120):
        """Generate realistic patients"""
        print(f"Generating {count} realistic patients...")

        for _ in range(count):
            # Generate realistic Romanian name
            name = fake.name()

            # Age distribution: more adults than children/elderly
            age_weights = [5, 15, 25, 30, 20, 5]  # 0-10, 11-25, 26-40, 41-55, 56-70, 71+
            age_group = random.choices(range(6), weights=age_weights)[0]

            if age_group == 0:
                age = random.randint(5, 10)
            elif age_group == 1:
                age = random.randint(11, 25)
            elif age_group == 2:
                age = random.randint(26, 40)
            elif age_group == 3:
                age = random.randint(41, 55)
            elif age_group == 4:
                age = random.randint(56, 70)
            else:
                age = random.randint(71, 85)

            birthdate = datetime.now() - timedelta(days=age * 365 + random.randint(0, 365))

            # First visit - usually within last 2-3 years for existing patients
            first_visit = fake.date_between(start_date='-3y', end_date='today')

            gender = random.choice(['M', 'F'])

            # Address and contact
            address = self.generate_realistic_address()
            phone = self.generate_realistic_phone()

            # Email (60% have email, more for younger patients)
            email = None
            if age < 50 and random.random() < 0.8:
                email_name = name.lower().replace(' ', '.').replace('ă', 'a').replace('î', 'i').replace('ș',
                                                                                                        's').replace(
                    'ț', 't').replace('â', 'a')
                email = f"{email_name}@{random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])}"
            elif age >= 50 and random.random() < 0.4:
                email_name = name.lower().replace(' ', '.').replace('ă', 'a').replace('î', 'i').replace('ș',
                                                                                                        's').replace(
                    'ț', 't').replace('â', 'a')
                email = f"{email_name}@{random.choice(['gmail.com', 'yahoo.com'])}"

            # Insurance
            insurance = random.choices(
                self.INSURANCE,
                weights=[30, 15, 15, 15, 10, 10, 5]  # CNAS most common
            )[0]

            self.cursor.execute('''
                INSERT INTO patients (patient_name, patient_birthdate, first_visit_at, gender, 
                                    address, phone, email, insurance, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, birthdate.strftime('%Y-%m-%d'), first_visit.strftime('%Y-%m-%d'),
                  gender, address, phone, email, insurance, 'Bucharest'))

    def generate_doctors(self):
        """Generate realistic doctors"""
        print("Generating realistic doctors...")

        for i, (name, specialty, education, experience) in enumerate(self.DOCTORS, 1):
            # Work schedule - most doctors work 5 days, some work 6
            work_days = random.choice([5, 6])

            # Room assignment
            room = f"Cabinet {i}"

            # Active status - 95% are active
            is_active = 1 if random.random() < 0.95 else 0

            # Phone and email
            phone = self.generate_realistic_phone()
            email_name = name.lower().replace('dr. ', '').replace(' ', '.').replace('ă', 'a').replace('î', 'i').replace(
                'ș', 's').replace('ț', 't').replace('â', 'a')
            email = f"{email_name}@dentalclinic.ro"

            self.cursor.execute('''
                INSERT INTO doctors (doctor_id, doctor_name, speciality, room, is_active,
                                   education, experience_years, work_days, phone, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (i, name, specialty, room, is_active, education, experience,
                  work_days, phone, email))

    def generate_procedures(self):
        """Generate procedures with realistic pricing"""
        print("Generating procedures...")

        for i, (name, category, duration, price_min, price_max) in enumerate(self.PROCEDURES, 1):
            self.cursor.execute('''
                INSERT INTO procedures (id, name, category, duration_minutes, price_min, price_max)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (i, name, category, duration, price_min, price_max))

    def generate_appointments(self, count=400):
        """Generate realistic appointments with business logic"""
        print(f"Generating {count} realistic appointments...")

        # Get patient and doctor counts
        self.cursor.execute("SELECT COUNT(*) FROM patients")
        patient_count = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM doctors WHERE is_active = 1")
        doctor_count = self.cursor.fetchone()[0]

        for i in range(count):
            patient_id = random.randint(1, patient_count)
            doctor_id = random.randint(1, doctor_count)

            # Generate appointment date - 70% in last 6 months, 20% in last year, 10% future
            date_choice = random.choices(['recent', 'past_year', 'future'], weights=[70, 20, 10])[0]

            if date_choice == 'recent':
                appointment_date = fake.date_between(start_date='-6m', end_date='today')
            elif date_choice == 'past_year':
                appointment_date = fake.date_between(start_date='-1y', end_date='-6m')
            else:
                appointment_date = fake.date_between(start_date='today', end_date='+3m')

            # Working hours: 8:00 - 19:00, appointments every 30 minutes
            working_hours = [(8, 0), (8, 30), (9, 0), (9, 30), (10, 0), (10, 30), (11, 0), (11, 30),
                             (12, 0), (12, 30), (13, 0), (13, 30), (14, 0), (14, 30), (15, 0), (15, 30),
                             (16, 0), (16, 30), (17, 0), (17, 30), (18, 0), (18, 30)]

            # Avoid lunch break (12:00-13:00)
            available_slots = [slot for slot in working_hours if not (slot[0] == 12 and slot[1] == 0)]

            start_hour, start_minute = random.choice(available_slots)
            start_time = f"{start_hour:02d}:{start_minute:02d}"

            # Choose procedure based on doctor specialty
            self.cursor.execute("SELECT speciality FROM doctors WHERE doctor_id = ?", (doctor_id,))
            doctor_specialty = self.cursor.fetchone()[0]

            # Filter procedures by specialty
            relevant_procedures = []
            for proc in self.PROCEDURES:
                if doctor_specialty == "General Dentistry":
                    if proc[1] in ['Diagnostic', 'Hygiene', 'Treatment']:
                        relevant_procedures.append(proc)
                elif doctor_specialty == "Orthodontics" and proc[1] == 'Orthodontics':
                    relevant_procedures.append(proc)
                elif doctor_specialty == "Endodontics" and proc[1] == 'Endodontics':
                    relevant_procedures.append(proc)
                elif doctor_specialty == "Oral Surgery" and proc[1] == 'Surgery':
                    relevant_procedures.append(proc)
                elif doctor_specialty == "Implantology" and proc[1] == 'Implantology':
                    relevant_procedures.append(proc)
                elif doctor_specialty == "Prosthodontics" and proc[1] == 'Prosthetics':
                    relevant_procedures.append(proc)
                elif doctor_specialty == "Aesthetic Dentistry" and proc[1] == 'Aesthetics':
                    relevant_procedures.append(proc)
                elif doctor_specialty == "Periodontics" and proc[1] == 'Periodontics':
                    relevant_procedures.append(proc)

            # If no specific procedures, fall back to general ones
            if not relevant_procedures:
                relevant_procedures = [proc for proc in self.PROCEDURES if
                                       proc[1] in ['Diagnostic', 'Hygiene', 'Treatment']]

            procedure = random.choice(relevant_procedures)
            procedure_name = procedure[0]
            procedure_category = procedure[1]
            duration = procedure[2]

            # Calculate end time
            end_datetime = datetime.combine(appointment_date, time(start_hour, start_minute)) + timedelta(
                minutes=duration)
            end_time = end_datetime.strftime('%H:%M')

            # Status distribution based on date
            if appointment_date > datetime.now().date():
                # Future appointments
                status = random.choices(['Confirmed', 'Pending'], weights=[80, 20])[0]
            elif appointment_date < datetime.now().date() - timedelta(days=7):
                # Past appointments
                status = random.choices(['Completed', 'Cancelled', 'No-Show'], weights=[85, 10, 5])[0]
            else:
                # Recent appointments
                status = random.choices(['Completed', 'Cancelled', 'Confirmed'], weights=[70, 15, 15])[0]

            # Appointment source
            source = random.choices(
                ['Phone', 'Online', 'Walk-in', 'Referral', 'Return Patient'],
                weights=[35, 30, 10, 15, 10]
            )[0]

            # Creation date (before appointment date)
            days_before = random.randint(1, 45)
            created_at = (appointment_date - timedelta(days=days_before)).strftime('%Y-%m-%d %H:%M:%S')

            # Notes for some appointments
            notes = None
            if random.random() < 0.3:  # 30% have notes
                notes_options = [
                    "Patient arrived on time",
                    "Slight delay due to traffic",
                    "Emergency appointment",
                    "Follow-up required in 2 weeks",
                    "Patient requested specific doctor",
                    "Insurance pre-authorization needed",
                    "Referred by Dr. Marinescu"
                ]
                notes = random.choice(notes_options)

            self.cursor.execute('''
                INSERT INTO appointments (id, patient_id, doctor_id, date, start_time, end_time,
                                        status, source, procedure_name, procedure_category, 
                                        created_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (i + 1, patient_id, doctor_id, appointment_date.strftime('%Y-%m-%d'),
                  start_time, end_time, status, source, procedure_name, procedure_category,
                  created_at, notes))

    def generate_payments(self):
        """Generate realistic payments for completed appointments"""
        print("Generating realistic payments...")

        # Get completed appointments
        self.cursor.execute("""
            SELECT id, procedure_name, date, patient_id 
            FROM appointments 
            WHERE status = 'Completed'
        """)
        completed_appointments = self.cursor.fetchall()

        for appointment_id, proc_name, appointment_date, patient_id in completed_appointments:
            # Get procedure price range
            self.cursor.execute("SELECT price_min, price_max FROM procedures WHERE name = ?", (proc_name,))
            price_range = self.cursor.fetchone()

            if price_range:
                # Generate realistic price within range
                price_min, price_max = price_range
                # Price usually closer to minimum for most patients
                if random.random() < 0.7:
                    amount = random.uniform(price_min, price_min + (price_max - price_min) * 0.6)
                else:
                    amount = random.uniform(price_min, price_max)
                amount = round(amount, 2)
            else:
                amount = random.uniform(150, 500)

            # Payment method distribution
            method = random.choices(
                ['Cash', 'Card', 'Bank Transfer', 'Insurance', 'Installments'],
                weights=[25, 45, 20, 8, 2]
            )[0]

            # Payment date - usually on appointment date or within a few days
            payment_delay = random.choices([0, 1, 2, 3, 7, 14, 30], weights=[60, 15, 10, 8, 4, 2, 1])[0]
            payment_date = datetime.strptime(appointment_date, '%Y-%m-%d') + timedelta(days=payment_delay)
            paid_at = payment_date.strftime('%Y-%m-%d %H:%M:%S')

            # Payment status
            status = 'Completed' if payment_delay <= 7 else random.choices(['Completed', 'Pending'], weights=[90, 10])[
                0]

            self.cursor.execute('''
                INSERT INTO payments (appointment_id, amount, method, paid_at, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (appointment_id, amount, method, paid_at, status))

    def generate_all_data(self):
        """Generate all realistic data"""
        print("🏥 Generating realistic data for Bucharest Dental Clinic...")
        print("=" * 60)

        # Clear existing data
        self.clear_existing_data()

        # Generate data in logical order
        self.generate_patients(120)
        self.generate_doctors()
        self.generate_procedures()
        self.generate_appointments(400)
        self.generate_payments()

        # Commit all changes
        self.conn.commit()

        print("=" * 60)
        print("✅ Data generation completed successfully!")
        print("\n📊 Generated data summary:")

        # Show summary
        tables = ['patients', 'doctors', 'procedures', 'appointments', 'payments']
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"   {table.capitalize()}: {count} records")

        print(f"\n💾 Database saved to: {PATH_DB}")
        print("🚀 Ready to run the application!")

    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Ensure database directory exists
    os.makedirs("database", exist_ok=True)

    # Generate realistic data
    generator = BucharestDentalClinicGenerator()
    try:
        generator.generate_all_data()
    finally:
        generator.close()