import sqlite3

PATH_DB = "database/dentalclinic.db"
conn = sqlite3.connect(PATH_DB)
cursor = conn.cursor()

print("🏥 Creating enhanced database schema for Bucharest Dental Clinic...")

# ENHANCED PATIENTS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients(
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    patient_birthdate TEXT NOT NULL,
    first_visit_at TEXT NOT NULL,
    gender TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    phone TEXT,
    email TEXT,
    insurance TEXT
)
''')

# ENHANCED DOCTORS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors(
    doctor_id INTEGER PRIMARY KEY,
    doctor_name TEXT NOT NULL,
    speciality TEXT NOT NULL,
    room TEXT NOT NULL,
    is_active BOOLEAN NOT NULL,
    education TEXT,
    experience_years INTEGER,
    work_days INTEGER,
    phone TEXT,
    email TEXT
)
''')

# PROCEDURES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS procedures (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    duration_minutes INTEGER,
    price_min REAL,
    price_max REAL
)
""")

# ENHANCED APPOINTMENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    date TEXT,
    start_time TEXT,
    end_time TEXT,
    status TEXT,
    source TEXT,
    procedure_name TEXT,
    procedure_category TEXT,
    created_at TEXT,
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
""")

# ENHANCED PAYMENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL,
    amount REAL,
    method TEXT,
    paid_at TEXT,
    status TEXT DEFAULT 'Completed',
    FOREIGN KEY (appointment_id) REFERENCES appointments(id)
)
""")

print("✅ Database schema created successfully!")
print("📋 Tables created:")
print("   - patients (enhanced with address, phone, email, insurance)")
print("   - doctors (enhanced with education, experience, contact)")
print("   - procedures (pricing and duration)")
print("   - appointments (enhanced with notes, source)")
print("   - payments (enhanced with status)")

conn.commit()
conn.close()

print("🚀 Ready to generate realistic data!")