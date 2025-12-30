import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from repositories.patient_repository import PatientRepository
from services.analytics_service import AnalyticsService
import sqlite3


class CliniTrackApp:
    # main application class for the GUI
    # keeping it simple but with all the main features

    def __init__(self, root):
        self.root = root
        self.root.title("CliniTrack - Clinic Management System")
        self.root.geometry("1000x700")

        # setup repositories
        self.patient_repo = PatientRepository()
        self.analytics = AnalyticsService()

        # create the main UI
        self.create_widgets()

    def create_widgets(self):
        # create all the UI elements

        # title label
        title = tk.Label(self.root, text="CliniTrack Management System",
                        font=("Arial", 18, "bold"), bg="#2c3e50", fg="white", pady=10)
        title.pack(fill=tk.X)

        # create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # add all the tabs
        self.create_patients_tab()
        self.create_doctors_tab()
        self.create_appointments_tab()
        self.create_payments_tab()
        self.create_stats_tab()

    def create_patients_tab(self):
        # tab for managing patients
        patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(patients_frame, text="Patients")

        # buttons panel
        button_panel = tk.Frame(patients_frame)
        button_panel.pack(pady=10, padx=10, fill=tk.X)

        tk.Button(button_panel, text="Add Patient", command=self.add_patient,
                 bg="#27ae60", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(button_panel, text="View Details", command=self.view_patient_details,
                 bg="#3498db", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(button_panel, text="Update Patient", command=self.update_patient,
                 bg="#f39c12", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        tk.Button(button_panel, text="Delete Patient", command=self.delete_patient,
                 bg="#e74c3c", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        # search panel
        search_panel = tk.Frame(patients_frame)
        search_panel.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(search_panel, text="Search by Name:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.patient_search_entry = tk.Entry(search_panel, font=("Arial", 10), width=30)
        self.patient_search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_panel, text="Search", command=self.search_patients,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        tk.Button(search_panel, text="Show All", command=self.show_all_patients,
                 bg="#2ecc71", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # patients list
        tree_frame = tk.Frame(patients_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.patient_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                        columns=("ID", "Name", "Age", "Gender", "City", "Phone", "Insurance"),
                                        show="headings")

        self.patient_tree.heading("ID", text="ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("City", text="City")
        self.patient_tree.heading("Phone", text="Phone")
        self.patient_tree.heading("Insurance", text="Insurance")

        self.patient_tree.column("ID", width=50)
        self.patient_tree.column("Name", width=180)
        self.patient_tree.column("Age", width=50)
        self.patient_tree.column("Gender", width=70)
        self.patient_tree.column("City", width=120)
        self.patient_tree.column("Phone", width=120)
        self.patient_tree.column("Insurance", width=100)

        self.patient_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.patient_tree.yview)

        self.patient_result_label = tk.Label(patients_frame, text="Click Show All to view patients",
                                            font=("Arial", 9), fg="gray")
        self.patient_result_label.pack(pady=5)

    def create_doctors_tab(self):
        # tab for viewing doctors
        doctors_frame = ttk.Frame(self.notebook)
        self.notebook.add(doctors_frame, text="Doctors")

        # refresh button
        tk.Button(doctors_frame, text="Refresh Doctors", command=self.load_doctors,
                 bg="#9b59b6", fg="white", font=("Arial", 10)).pack(pady=10)

        # doctors list
        tree_frame = tk.Frame(doctors_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.doctor_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                       columns=("ID", "Name", "Specialty", "Room", "Experience", "Active"),
                                       show="headings")

        self.doctor_tree.heading("ID", text="ID")
        self.doctor_tree.heading("Name", text="Name")
        self.doctor_tree.heading("Specialty", text="Specialty")
        self.doctor_tree.heading("Room", text="Room")
        self.doctor_tree.heading("Experience", text="Years Exp")
        self.doctor_tree.heading("Active", text="Status")

        self.doctor_tree.column("ID", width=50)
        self.doctor_tree.column("Name", width=180)
        self.doctor_tree.column("Specialty", width=150)
        self.doctor_tree.column("Room", width=100)
        self.doctor_tree.column("Experience", width=80)
        self.doctor_tree.column("Active", width=80)

        self.doctor_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.doctor_tree.yview)

    def create_appointments_tab(self):
        # tab for viewing appointments
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text="Appointments")

        # search panel
        search_panel = tk.Frame(appointments_frame)
        search_panel.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(search_panel, text="Patient ID:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.appt_patient_id_entry = tk.Entry(search_panel, font=("Arial", 10), width=10)
        self.appt_patient_id_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_panel, text="View Patient Appointments", command=self.view_patient_appointments,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        tk.Button(search_panel, text="Show All Appointments", command=self.show_all_appointments,
                 bg="#2ecc71", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # appointments list
        tree_frame = tk.Frame(appointments_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.appt_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                     columns=("ID", "Patient ID", "Doctor ID", "Date", "Time", "Procedure", "Status"),
                                     show="headings")

        self.appt_tree.heading("ID", text="ID")
        self.appt_tree.heading("Patient ID", text="Patient ID")
        self.appt_tree.heading("Doctor ID", text="Doctor ID")
        self.appt_tree.heading("Date", text="Date")
        self.appt_tree.heading("Time", text="Time")
        self.appt_tree.heading("Procedure", text="Procedure")
        self.appt_tree.heading("Status", text="Status")

        self.appt_tree.column("ID", width=50)
        self.appt_tree.column("Patient ID", width=80)
        self.appt_tree.column("Doctor ID", width=80)
        self.appt_tree.column("Date", width=100)
        self.appt_tree.column("Time", width=80)
        self.appt_tree.column("Procedure", width=200)
        self.appt_tree.column("Status", width=100)

        self.appt_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.appt_tree.yview)

        self.appt_result_label = tk.Label(appointments_frame, text="Enter patient ID or click Show All",
                                         font=("Arial", 9), fg="gray")
        self.appt_result_label.pack(pady=5)

    def create_payments_tab(self):
        # tab for viewing payments
        payments_frame = ttk.Frame(self.notebook)
        self.notebook.add(payments_frame, text="Payments")

        # refresh button
        tk.Button(payments_frame, text="Show All Payments", command=self.load_payments,
                 bg="#27ae60", fg="white", font=("Arial", 10)).pack(pady=10)

        # payments list
        tree_frame = tk.Frame(payments_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.payment_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                        columns=("ID", "Appt ID", "Amount", "Method", "Date", "Status"),
                                        show="headings")

        self.payment_tree.heading("ID", text="ID")
        self.payment_tree.heading("Appt ID", text="Appointment ID")
        self.payment_tree.heading("Amount", text="Amount (RON)")
        self.payment_tree.heading("Method", text="Payment Method")
        self.payment_tree.heading("Date", text="Date")
        self.payment_tree.heading("Status", text="Status")

        self.payment_tree.column("ID", width=50)
        self.payment_tree.column("Appt ID", width=100)
        self.payment_tree.column("Amount", width=120)
        self.payment_tree.column("Method", width=120)
        self.payment_tree.column("Date", width=120)
        self.payment_tree.column("Status", width=100)

        self.payment_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.payment_tree.yview)

        self.payment_result_label = tk.Label(payments_frame, text="",
                                            font=("Arial", 9), fg="gray")
        self.payment_result_label.pack(pady=5)

    def create_stats_tab(self):
        # tab for showing statistics
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Analytics Dashboard")

        # refresh button
        tk.Button(stats_frame, text="Refresh Statistics", command=self.load_statistics,
                 bg="#9b59b6", fg="white", font=("Arial", 10)).pack(pady=10)

        # stats text area
        text_frame = tk.Frame(stats_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_text = tk.Text(text_frame, font=("Courier", 9),
                                 yscrollcommand=scrollbar.set, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.stats_text.yview)

    # patient management functions
    def add_patient(self):
        # opens a dialog to add a new patient
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Patient")
        dialog.geometry("400x350")

        # form fields
        tk.Label(dialog, text="Patient Name:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(dialog, font=("Arial", 10), width=25)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(dialog, text="Birthdate (YYYY-MM-DD):", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        birthdate_entry = tk.Entry(dialog, font=("Arial", 10), width=25)
        birthdate_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(dialog, text="First Visit (YYYY-MM-DD):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        first_visit_entry = tk.Entry(dialog, font=("Arial", 10), width=25)
        first_visit_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(dialog, text="Gender (M/F):", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        gender_entry = tk.Entry(dialog, font=("Arial", 10), width=25)
        gender_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(dialog, text="City:", font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
        city_entry = tk.Entry(dialog, font=("Arial", 10), width=25)
        city_entry.grid(row=4, column=1, padx=10, pady=10)

        def save_patient():
            name = name_entry.get().strip()
            birthdate = birthdate_entry.get().strip()
            first_visit = first_visit_entry.get().strip()
            gender = gender_entry.get().strip().upper()
            city = city_entry.get().strip()

            if not all([name, birthdate, first_visit, gender, city]):
                messagebox.showwarning("Missing Data", "Please fill in all fields")
                return

            patient_data = {
                'name': name,
                'birthdate': birthdate,
                'first_visit': first_visit,
                'gender': gender,
                'city': city
            }

            try:
                patient_id = self.patient_repo.create(patient_data)
                messagebox.showinfo("Success", f"Patient added successfully with ID: {patient_id}")
                dialog.destroy()
                self.show_all_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add patient: {str(e)}")

        tk.Button(dialog, text="Save Patient", command=save_patient,
                 bg="#27ae60", fg="white", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=20)

    def update_patient(self):
        # updates selected patient information
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to update")
            return

        item = self.patient_tree.item(selected[0])
        patient_id = item['values'][0]

        # get patient data
        patient = self.patient_repo.read(patient_id)
        if not patient:
            messagebox.showerror("Error", "Patient not found")
            return

        # create update dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Patient")
        dialog.geometry("400x250")

        tk.Label(dialog, text=f"Updating Patient ID: {patient_id}", font=("Arial", 12, "bold")).pack(pady=10)

        # form fields
        form_frame = tk.Frame(dialog)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        name_entry.insert(0, patient.patient_name)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="City:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        city_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        city_entry.insert(0, patient.city)
        city_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Gender (M/F):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        gender_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        gender_entry.insert(0, patient.gender)
        gender_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_updates():
            updates = {}
            new_name = name_entry.get().strip()
            new_city = city_entry.get().strip()
            new_gender = gender_entry.get().strip().upper()

            if new_name != patient.patient_name:
                updates['patient_name'] = new_name
            if new_city != patient.city:
                updates['city'] = new_city
            if new_gender != patient.gender:
                updates['gender'] = new_gender

            if not updates:
                messagebox.showinfo("No Changes", "No changes were made")
                dialog.destroy()
                return

            try:
                self.patient_repo.update(patient_id, updates)
                messagebox.showinfo("Success", "Patient updated successfully")
                dialog.destroy()
                self.show_all_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update patient: {str(e)}")

        tk.Button(dialog, text="Save Changes", command=save_updates,
                 bg="#f39c12", fg="white", font=("Arial", 10)).pack(pady=20)

    def delete_patient(self):
        # deletes selected patient
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to delete")
            return

        item = self.patient_tree.item(selected[0])
        patient_id = item['values'][0]
        patient_name = item['values'][1]

        confirm = messagebox.askyesno("Confirm Delete",
                                      f"Are you sure you want to delete patient '{patient_name}'?")

        if confirm:
            try:
                self.patient_repo.delete(patient_id)
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.show_all_patients()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")

    def view_patient_details(self):
        # shows detailed analytics for selected patient
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a patient to view details")
            return

        item = self.patient_tree.item(selected[0])
        patient_id = item['values'][0]

        # get patient data
        patient = self.patient_repo.read(patient_id)
        if not patient:
            messagebox.showerror("Error", "Patient not found")
            return

        # get appointment and payment data
        conn = sqlite3.connect("database/dentalclinic.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = ?", (patient_id,))
        total_appts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = ? AND status = 'Completed'", (patient_id,))
        completed = cursor.fetchone()[0]

        cursor.execute("""
            SELECT SUM(p.amount)
            FROM payments p
            JOIN appointments a ON p.appointment_id = a.id
            WHERE a.patient_id = ?
        """, (patient_id,))
        total_spent = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT date, procedure_name FROM appointments
            WHERE patient_id = ? ORDER BY date DESC LIMIT 1
        """, (patient_id,))
        last_appt = cursor.fetchone()

        conn.close()

        # show details dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Patient Details - {patient.patient_name}")
        dialog.geometry("500x400")

        text = tk.Text(dialog, font=("Courier", 10), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text.insert(tk.END, "=" * 50 + "\n")
        text.insert(tk.END, f"PATIENT ANALYTICS - {patient.patient_name}\n")
        text.insert(tk.END, "=" * 50 + "\n\n")

        text.insert(tk.END, f"Patient ID: {patient.patient_id}\n")
        text.insert(tk.END, f"Age: {patient.get_age()} years\n")
        text.insert(tk.END, f"Gender: {patient.gender}\n")
        text.insert(tk.END, f"City: {patient.city}\n")
        text.insert(tk.END, f"Phone: {patient.phone or 'N/A'}\n")
        text.insert(tk.END, f"Email: {patient.email or 'N/A'}\n")
        text.insert(tk.END, f"Insurance: {patient.insurance or 'None'}\n")
        text.insert(tk.END, f"First Visit: {patient.first_visit_at}\n\n")

        text.insert(tk.END, "--- Appointment History ---\n")
        text.insert(tk.END, f"Total Appointments: {total_appts}\n")
        text.insert(tk.END, f"Completed: {completed}\n")
        text.insert(tk.END, f"Cancelled/Other: {total_appts - completed}\n\n")

        if last_appt:
            text.insert(tk.END, f"Last Visit: {last_appt[0]} ({last_appt[1]})\n\n")

        text.insert(tk.END, "--- Financial Summary ---\n")
        text.insert(tk.END, f"Total Spent: {total_spent:,.2f} RON\n")
        if completed > 0:
            avg = total_spent / completed
            text.insert(tk.END, f"Average Per Visit: {avg:,.2f} RON\n")

        text.config(state=tk.DISABLED)

    def search_patients(self):
        # search for patients by name
        name = self.patient_search_entry.get().strip()

        if not name:
            messagebox.showwarning("Input Required", "Please enter a name to search")
            return

        # clear existing results
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        # search in database
        patients = self.patient_repo.search_by_name(name)

        # show results
        if patients:
            for patient in patients:
                age = patient.get_age()
                phone = patient.phone if patient.phone else "N/A"
                insurance = patient.insurance if patient.insurance else "None"

                self.patient_tree.insert("", tk.END, values=(
                    patient.patient_id,
                    patient.patient_name,
                    age,
                    patient.gender,
                    patient.city,
                    phone,
                    insurance
                ))

            self.patient_result_label.config(text=f"Found {len(patients)} patient(s)")
        else:
            self.patient_result_label.config(text="No patients found")

    def show_all_patients(self):
        # show all patients in database
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        patients = self.patient_repo.get_all()

        if patients:
            for patient in patients:
                age = patient.get_age()
                phone = patient.phone if patient.phone else "N/A"
                insurance = patient.insurance if patient.insurance else "None"

                self.patient_tree.insert("", tk.END, values=(
                    patient.patient_id,
                    patient.patient_name,
                    age,
                    patient.gender,
                    patient.city,
                    phone,
                    insurance
                ))

            self.patient_result_label.config(text=f"Showing all {len(patients)} patients")
        else:
            self.patient_result_label.config(text="No patients in database")

    def load_doctors(self):
        # loads and displays all doctors
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)

        conn = sqlite3.connect("database/dentalclinic.db")
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_id, doctor_name, speciality, room, experience_years, is_active FROM doctors")
        doctors = cursor.fetchall()
        conn.close()

        for doctor in doctors:
            status = "Active" if doctor[5] else "Inactive"
            self.doctor_tree.insert("", tk.END, values=(
                doctor[0], doctor[1], doctor[2], doctor[3], doctor[4], status
            ))

    def view_patient_appointments(self):
        # view appointments for a specific patient
        patient_id = self.appt_patient_id_entry.get().strip()

        if not patient_id:
            messagebox.showwarning("Input Required", "Please enter a patient ID")
            return

        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)

        conn = sqlite3.connect("database/dentalclinic.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, patient_id, doctor_id, date, start_time, procedure_name, status
            FROM appointments WHERE patient_id = ? ORDER BY date DESC
        """, (patient_id,))
        appointments = cursor.fetchall()
        conn.close()

        if appointments:
            for appt in appointments:
                self.appt_tree.insert("", tk.END, values=appt)
            self.appt_result_label.config(text=f"Found {len(appointments)} appointment(s) for patient {patient_id}")
        else:
            self.appt_result_label.config(text=f"No appointments found for patient {patient_id}")

    def show_all_appointments(self):
        # shows all appointments in the system
        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)

        conn = sqlite3.connect("database/dentalclinic.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, patient_id, doctor_id, date, start_time, procedure_name, status
            FROM appointments ORDER BY date DESC LIMIT 200
        """)
        appointments = cursor.fetchall()
        conn.close()

        if appointments:
            for appt in appointments:
                self.appt_tree.insert("", tk.END, values=appt)
            self.appt_result_label.config(text=f"Showing {len(appointments)} most recent appointments")
        else:
            self.appt_result_label.config(text="No appointments found")

    def load_payments(self):
        # loads and displays all payments
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        conn = sqlite3.connect("database/dentalclinic.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, appointment_id, amount, method, paid_at, status
            FROM payments ORDER BY paid_at DESC LIMIT 200
        """)
        payments = cursor.fetchall()
        conn.close()

        total = 0
        for payment in payments:
            self.payment_tree.insert("", tk.END, values=payment)
            total += payment[2]

        self.payment_result_label.config(text=f"Showing {len(payments)} payments - Total: {total:,.2f} RON")

    def load_statistics(self):
        # load and display comprehensive statistics
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Loading statistics...\n\n")

        summary = self.analytics.get_dashboard_summary()

        self.stats_text.delete(1.0, tk.END)

        # patient demographics
        if summary['demographics']:
            demo = summary['demographics']
            self.stats_text.insert(tk.END, "=" * 60 + "\n")
            self.stats_text.insert(tk.END, "PATIENT DEMOGRAPHICS\n")
            self.stats_text.insert(tk.END, "=" * 60 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Patients: {demo['total_patients']}\n\n")

            self.stats_text.insert(tk.END, "Age Groups:\n")
            for group, count in demo['age_groups'].items():
                self.stats_text.insert(tk.END, f"  {group}: {count}\n")

            self.stats_text.insert(tk.END, "\nGender Distribution:\n")
            for gender, count in demo['gender'].items():
                self.stats_text.insert(tk.END, f"  {gender}: {count}\n")

            self.stats_text.insert(tk.END, "\n\n")

        # appointment stats
        if summary['appointments']:
            appt = summary['appointments']
            self.stats_text.insert(tk.END, "=" * 60 + "\n")
            self.stats_text.insert(tk.END, "APPOINTMENT STATISTICS\n")
            self.stats_text.insert(tk.END, "=" * 60 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Appointments: {appt['total_appointments']}\n\n")

            self.stats_text.insert(tk.END, "Status Distribution:\n")
            for status, count in appt['status_distribution'].items():
                self.stats_text.insert(tk.END, f"  {status}: {count}\n")

            self.stats_text.insert(tk.END, "\n\n")

        # revenue stats
        if summary['revenue']:
            rev = summary['revenue']
            self.stats_text.insert(tk.END, "=" * 60 + "\n")
            self.stats_text.insert(tk.END, "PAYMENT & REVENUE ANALYSIS\n")
            self.stats_text.insert(tk.END, "=" * 60 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Revenue: {rev['total_revenue']:,.2f} RON\n")
            self.stats_text.insert(tk.END, f"Average Payment: {rev['average_payment']:,.2f} RON\n\n")

            self.stats_text.insert(tk.END, "Top 5 Procedures by Revenue:\n")
            for proc, amount in rev['top_procedures']:
                self.stats_text.insert(tk.END, f"  {proc}: {amount:,.2f} RON\n")

            self.stats_text.insert(tk.END, "\n\n")

        # doctor performance
        if summary['doctor_performance']:
            self.stats_text.insert(tk.END, "=" * 60 + "\n")
            self.stats_text.insert(tk.END, "DOCTOR PERFORMANCE\n")
            self.stats_text.insert(tk.END, "=" * 60 + "\n\n")

            for doc in summary['doctor_performance']:
                self.stats_text.insert(tk.END, f"{doc['name']} ({doc['specialty']})\n")
                self.stats_text.insert(tk.END, f"  Total Appointments: {doc['total_appointments']}\n")
                self.stats_text.insert(tk.END, f"  Completed: {doc['completed']}\n")
                self.stats_text.insert(tk.END, f"  Completion Rate: {doc['completion_rate']}%\n\n")


def main():
    # entry point for the GUI application
    root = tk.Tk()
    app = CliniTrackApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
