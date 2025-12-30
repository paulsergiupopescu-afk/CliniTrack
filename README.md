# CliniTrack

A dental clinic management and analytics system built with Python. CliniTrack helps manage patients, doctors, appointments and provides business insights through data analytics.

## What it does

- Manage patient records (add, update, delete, search)
- Search patients by name
- View individual patient analytics (appointment history, spending)
- Track doctors and their specialties
- Handle appointments and scheduling
- Payment tracking
- Analytics dashboard with various statistics

## Features I'm proud of

### Patient Management
Complete CRUD operations - you can add patients, search for them by ID or name, update their info, and delete records. Also includes individual patient analytics showing appointment history, total spending, and visit statistics.

### Analytics
This is the part I spent most time on. The system can show:
- Patient demographics (age groups, gender distribution)
- Appointment trends over time
- Peak hours and busiest days
- Revenue analysis
- Doctor performance metrics

### GUI Application
Built a complete management system using tkinter with 5 main tabs:
- **Patients**: Add, update, delete, search patients by name, view detailed patient analytics
- **Doctors**: View all doctors with their specialties and experience
- **Appointments**: View all appointments or filter by patient, track appointment history
- **Payments**: View payment records with totals and revenue tracking
- **Analytics Dashboard**: Comprehensive statistics including demographics, revenue, and doctor performance

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/CliniTrack.git
cd CliniTrack
```

2. Install dependencies (optional - only needed for data generation)
```bash
pip install -r requirements.txt
```

3. Run the application

## How to run

### GUI Application (Recommended)
```bash
python gui_app.py
```
This launches the graphical interface where you can search patients and view statistics.

### Quick analytics demo
```bash
python test_analytics.py
```
This shows all the analytics in one go.

### Interactive analytics menu
```bash
python analytics_demo.py
```
Lets you choose what analytics to see.

### Patient management (CLI)
```bash
python main.py
```
CRUD interface for managing patients in the terminal.

## Project structure

```
CliniTrack/
├── models/                 # data models (Patient, Doctor, Appointment, etc)
├── repositories/          # database operations
├── services/              # analytics logic
├── database/              # SQLite database + data generator
├── main.py               # patient management CLI
├── analytics_demo.py     # analytics showcase
└── test_analytics.py     # quick analytics test
```

## Tech stack

- Python 3.14
- SQLite for the database
- Faker for generating test data (Romanian names and addresses)

## Database

The database has:
- 102 patients
- 10 doctors with different specialties
- 250 appointments
- 185 payment records

All data is generated using Faker library to simulate a real clinic in Bucharest.

## What I learned

- Repository pattern for organizing database code
- Working with SQLite and SQL queries
- Data analysis and aggregation
- Building CLI applications
- Code organization and structure

## Future improvements

Things I want to add:
- Charts and visualizations (maybe with matplotlib)
- REST API with FastAPI
- Better error handling
- More detailed reports
- Export to PDF or CSV

## Notes

- This is a learning project built while studying Python
- All patient data is fake (generated with Faker)
- Focus was on clean code structure and analytics features

---

Built while learning Python and software development patterns.
