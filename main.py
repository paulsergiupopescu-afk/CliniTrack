from repositories.patient_repository import PatientRepository
from repositories.doctor_repository import DoctorRepository
from repositories.appointment_repository import AppointmentRepository
from repositories.payment_repository import PaymentRepository


def print_header(title):
    # prints a nice header for menu sections
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def clear_screen():
    # clears the screen by printing newlines
    print("\n" * 2)


# ===== PATIENT FUNCTIONS =====

def add_patient():
    # adds a new patient to the database
    print_header("ADD NEW PATIENT")

    name = input("Name: ")
    birthdate = input("Birthdate (YYYY-MM-DD): ")
    first_visit = input("First visit (YYYY-MM-DD): ")
    gender = input("Gender (M/F): ").upper()
    city = input("City: ")

    patient_data = {
        'name': name,
        'birthdate': birthdate,
        'first_visit': first_visit,
        'gender': gender,
        'city': city
    }

    repo = PatientRepository()
    patient_id = repo.create(patient_data)

    print(f"\nPatient created with ID: {patient_id}")
    input("\nPress Enter to continue...")


def search_patient():
    # search for a patient by their ID
    print_header("SEARCH PATIENT")

    patient_id = int(input("Enter patient ID: "))

    repo = PatientRepository()
    patient = repo.read(patient_id)

    if patient:
        print(f"\nPatient found:")
        print(f"   ID: {patient.patient_id}")
        print(f"   Name: {patient.patient_name}")  # FIXED: was patient.name
        print(f"   Birthdate: {patient.patient_birthdate}")  # FIXED: was patient.birthdate
        print(f"   First Visit: {patient.first_visit_at}")  # FIXED: was patient.first_visit
        print(f"   Gender: {patient.gender}")
        print(f"   City: {patient.city}")
    else:
        print(f"\nPatient with ID {patient_id} not found!")

    input("\nPress Enter to continue...")


def update_patient():
    # updates patient information
    print_header("UPDATE PATIENT")

    patient_id = int(input("Enter patient ID: "))

    repo = PatientRepository()
    patient = repo.read(patient_id)

    if not patient:
        print(f"\nPatient with ID {patient_id} not found!")
        input("\nPress Enter to continue...")
        return

    print(f"\nCurrent data:")
    print(f"   Name: {patient.patient_name}")  # FIXED: was patient.name
    print(f"   City: {patient.city}")
    print(f"   Gender: {patient.gender}")

    print("\nEnter new values (press Enter to skip):")

    new_name = input(f"New name [{patient.patient_name}]: ").strip()  # FIXED: was patient.name
    new_city = input(f"New city [{patient.city}]: ").strip()
    new_gender = input(f"New gender [{patient.gender}]: ").strip().upper()

    updates = {}
    if new_name:
        updates['patient_name'] = new_name
    if new_city:
        updates['city'] = new_city
    if new_gender:
        updates['gender'] = new_gender

    if updates:
        repo.update(patient_id, updates)
        print("\nPatient updated successfully!")
    else:
        print("\nNo changes made")

    input("\nPress Enter to continue...")


def delete_patient():
    # deletes a patient from the database
    print_header("DELETE PATIENT")

    patient_id = int(input("Enter patient ID to delete: "))

    repo = PatientRepository()
    patient = repo.read(patient_id)

    if not patient:
        print(f"\nPatient with ID {patient_id} not found!")
        input("\nPress Enter to continue...")
        return

    print(f"\nAre you sure you want to delete: {patient.patient_name}?")  # FIXED: was patient.name
    confirm = input("Type 'yes' to confirm: ").lower()

    if confirm == 'yes':
        repo.delete(patient_id)
        print("\nPatient deleted successfully!")
    else:
        print("\nDeletion cancelled")

    input("\nPress Enter to continue...")


def view_all_patients():
    # shows all patients in the database
    print_header("ALL PATIENTS")

    repo = PatientRepository()
    patients = repo.get_all()

    if not patients:
        print("\nNo patients in database!")
    else:
        print(f"\n{'ID':<5} {'Name':<25} {'City':<15} {'Gender':<8}")
        print("-" * 60)
        for p in patients:
            print(f"{p.patient_id:<5} {p.patient_name:<25} {p.city:<15} {p.gender:<8}")  # FIXED: was p.name
        print("-" * 60)
        print(f"\nTotal patients: {len(patients)}")

    input("\nPress Enter to continue...")


def patient_analytics():
    """Show analytics for a specific patient"""
    print_header("PATIENT ANALYTICS")

    patient_id = int(input("Enter patient ID: "))

    # get patient info
    patient_repo = PatientRepository()
    patient = patient_repo.read(patient_id)

    if not patient:
        print(f"\nPatient with ID {patient_id} not found!")
        input("\nPress Enter to continue...")
        return

    # show basic patient info
    print(f"\nPatient: {patient.patient_name}")
    print(f"Age: {patient.get_age()} years")
    print(f"Gender: {patient.gender}")
    print(f"City: {patient.city}")
    print(f"First visit: {patient.first_visit_at}")

    # get appointments for this patient
    # doing it simple - just count from database
    import sqlite3
    conn = sqlite3.connect("database/dentalclinic.db")
    cursor = conn.cursor()

    # count appointments
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = ?", (patient_id,))
    total_appointments = cursor.fetchone()[0]

    # count completed
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = ? AND status = 'Completed'", (patient_id,))
    completed = cursor.fetchone()[0]

    # get last appointment
    cursor.execute("SELECT date, procedure_name FROM appointments WHERE patient_id = ? ORDER BY date DESC LIMIT 1", (patient_id,))
    last_appt = cursor.fetchone()

    # get total spent (payments for this patient)
    cursor.execute("""
        SELECT SUM(p.amount)
        FROM payments p
        JOIN appointments a ON p.appointment_id = a.id
        WHERE a.patient_id = ?
    """, (patient_id,))
    total_spent = cursor.fetchone()[0]

    conn.close()

    # show appointment stats
    print("\n--- Appointment History ---")
    print(f"Total appointments: {total_appointments}")
    print(f"Completed: {completed}")
    print(f"Cancelled/Other: {total_appointments - completed}")

    if last_appt:
        print(f"Last visit: {last_appt[0]} ({last_appt[1]})")

    # show spending
    if total_spent:
        print(f"\nTotal spent: {total_spent:,.2f} RON")
        if completed > 0:
            avg_per_visit = total_spent / completed
            print(f"Average per visit: {avg_per_visit:,.2f} RON")

    input("\nPress Enter to continue...")


# ===== MENUS =====

def patient_menu():
    # menu for patient management options
    while True:
        clear_screen()
        print_header("PATIENT MANAGEMENT")
        print("\n1. Add Patient")
        print("2. Search Patient")
        print("3. Update Patient")
        print("4. Delete Patient")
        print("5. View All Patients")
        print("6. Patient Analytics")
        print("0. Back to Main Menu")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            add_patient()
        elif choice == '2':
            search_patient()
        elif choice == '3':
            update_patient()
        elif choice == '4':
            delete_patient()
        elif choice == '5':
            view_all_patients()
        elif choice == '6':
            patient_analytics()
        elif choice == '0':
            break
        else:
            print("\nInvalid option!")
            input("Press Enter to continue...")


def main_menu():
    # main menu of the application
    while True:
        clear_screen()
        print_header("CLINITRACK - PATIENT MANAGEMENT")
        print("\n1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Payment Management")
        print("0. Exit")

        choice = input("\nChoose: ").strip()

        if choice == '1':
            patient_menu()
        elif choice == '2':
            print("\nDoctor management - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '3':
            print("\nAppointment management - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '4':
            print("\nPayment management - Coming soon!")
            input("Press Enter to continue...")
        elif choice == '0':
            clear_screen()
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid option!")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()