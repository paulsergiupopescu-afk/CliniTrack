import tkinter as tk
from tkinter import ttk, messagebox
from repositories.patient_repository import PatientRepository
from services.analytics_service import AnalyticsService


class CliniTrackApp:
    # main application class for the GUI
    # keeping it simple - just what we need

    def __init__(self, root):
        self.root = root
        self.root.title("CliniTrack - Patient Management")
        self.root.geometry("900x600")

        # setup repositories
        self.patient_repo = PatientRepository()
        self.analytics = AnalyticsService()

        # create the main UI
        self.create_widgets()

    def create_widgets(self):
        # create all the UI elements

        # title label
        title = tk.Label(self.root, text="CliniTrack System",
                        font=("Arial", 18, "bold"), bg="#2c3e50", fg="white", pady=10)
        title.pack(fill=tk.X)

        # create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # add tabs
        self.create_search_tab()
        self.create_stats_tab()

    def create_search_tab(self):
        # tab for searching patients
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="Search Patients")

        # search controls
        search_control = tk.Frame(search_frame)
        search_control.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(search_control, text="Patient Name:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(search_control, font=("Arial", 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(search_control, text="Search", command=self.search_patients,
                              bg="#3498db", fg="white", font=("Arial", 10))
        search_btn.pack(side=tk.LEFT, padx=5)

        show_all_btn = tk.Button(search_control, text="Show All", command=self.show_all_patients,
                                bg="#2ecc71", fg="white", font=("Arial", 10))
        show_all_btn.pack(side=tk.LEFT, padx=5)

        # results tree
        tree_frame = tk.Frame(search_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # treeview for patient list
        self.patient_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set,
                                        columns=("ID", "Name", "Age", "Gender", "City", "Phone"),
                                        show="headings")

        # configure columns
        self.patient_tree.heading("ID", text="ID")
        self.patient_tree.heading("Name", text="Name")
        self.patient_tree.heading("Age", text="Age")
        self.patient_tree.heading("Gender", text="Gender")
        self.patient_tree.heading("City", text="City")
        self.patient_tree.heading("Phone", text="Phone")

        self.patient_tree.column("ID", width=50)
        self.patient_tree.column("Name", width=200)
        self.patient_tree.column("Age", width=60)
        self.patient_tree.column("Gender", width=80)
        self.patient_tree.column("City", width=150)
        self.patient_tree.column("Phone", width=120)

        self.patient_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.patient_tree.yview)

        # info label
        self.result_label = tk.Label(search_frame, text="Enter a name to search or click Show All",
                                    font=("Arial", 9), fg="gray")
        self.result_label.pack(pady=5)

    def create_stats_tab(self):
        # tab for showing statistics
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")

        # refresh button
        refresh_btn = tk.Button(stats_frame, text="Refresh Stats", command=self.load_statistics,
                               bg="#9b59b6", fg="white", font=("Arial", 10))
        refresh_btn.pack(pady=10)

        # create a text widget to show stats
        text_frame = tk.Frame(stats_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stats_text = tk.Text(text_frame, font=("Courier", 10),
                                 yscrollcommand=scrollbar.set, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.stats_text.yview)

    def search_patients(self):
        # search for patients by name
        name = self.search_entry.get().strip()

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
                # calculate age - doing it simple
                age = patient.get_age()
                phone = patient.phone if patient.phone else "N/A"

                self.patient_tree.insert("", tk.END, values=(
                    patient.patient_id,
                    patient.patient_name,
                    age,
                    patient.gender,
                    patient.city,
                    phone
                ))

            self.result_label.config(text=f"Found {len(patients)} patient(s)")
        else:
            self.result_label.config(text="No patients found")

    def show_all_patients(self):
        # show all patients in database

        # clear existing results
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        # get all patients
        patients = self.patient_repo.get_all()

        # display them
        if patients:
            for patient in patients:
                age = patient.get_age()
                phone = patient.phone if patient.phone else "N/A"

                self.patient_tree.insert("", tk.END, values=(
                    patient.patient_id,
                    patient.patient_name,
                    age,
                    patient.gender,
                    patient.city,
                    phone
                ))

            self.result_label.config(text=f"Showing all {len(patients)} patients")
        else:
            self.result_label.config(text="No patients in database")

    def load_statistics(self):
        # load and display statistics

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Loading statistics...\n\n")

        # get all stats
        summary = self.analytics.get_dashboard_summary()

        # clear and show new stats
        self.stats_text.delete(1.0, tk.END)

        # patient demographics
        if summary['demographics']:
            demo = summary['demographics']
            self.stats_text.insert(tk.END, "=" * 50 + "\n")
            self.stats_text.insert(tk.END, "PATIENT DEMOGRAPHICS\n")
            self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Patients: {demo['total_patients']}\n\n")

            self.stats_text.insert(tk.END, "Age Groups:\n")
            for group, count in demo['age_groups'].items():
                self.stats_text.insert(tk.END, f"  {group}: {count}\n")

            self.stats_text.insert(tk.END, "\nGender Distribution:\n")
            for gender, count in demo['gender'].items():
                self.stats_text.insert(tk.END, f"  {gender}: {count}\n")

            self.stats_text.insert(tk.END, "\n")

        # appointment stats
        if summary['appointments']:
            appt = summary['appointments']
            self.stats_text.insert(tk.END, "=" * 50 + "\n")
            self.stats_text.insert(tk.END, "APPOINTMENT STATISTICS\n")
            self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Appointments: {appt['total_appointments']}\n\n")

            self.stats_text.insert(tk.END, "Status Distribution:\n")
            for status, count in appt['status_distribution'].items():
                self.stats_text.insert(tk.END, f"  {status}: {count}\n")

            self.stats_text.insert(tk.END, "\n")

        # revenue stats
        if summary['revenue']:
            rev = summary['revenue']
            self.stats_text.insert(tk.END, "=" * 50 + "\n")
            self.stats_text.insert(tk.END, "REVENUE ANALYSIS\n")
            self.stats_text.insert(tk.END, "=" * 50 + "\n\n")
            self.stats_text.insert(tk.END, f"Total Revenue: {rev['total_revenue']:,.2f} RON\n")
            self.stats_text.insert(tk.END, f"Average Payment: {rev['average_payment']:,.2f} RON\n\n")

            self.stats_text.insert(tk.END, "Top 5 Procedures by Revenue:\n")
            for proc, amount in rev['top_procedures']:
                self.stats_text.insert(tk.END, f"  {proc}: {amount:,.2f} RON\n")

            self.stats_text.insert(tk.END, "\n")

        # doctor performance
        if summary['doctor_performance']:
            self.stats_text.insert(tk.END, "=" * 50 + "\n")
            self.stats_text.insert(tk.END, "DOCTOR PERFORMANCE\n")
            self.stats_text.insert(tk.END, "=" * 50 + "\n\n")

            for doc in summary['doctor_performance']:
                self.stats_text.insert(tk.END, f"{doc['name']} ({doc['specialty']})\n")
                self.stats_text.insert(tk.END, f"  Total Appointments: {doc['total_appointments']}\n")
                self.stats_text.insert(tk.END, f"  Completed: {doc['completed']}\n")
                self.stats_text.insert(tk.END, f"  Completion Rate: {doc['completion_rate']}%\n\n")


def main():
    # entry point for the GUI app
    root = tk.Tk()
    app = CliniTrackApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
