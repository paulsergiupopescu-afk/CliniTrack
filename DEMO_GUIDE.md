# CliniTrack - Demo Guide

Quick guide for running CliniTrack demos.

## Run the demos

### Analytics test (fastest)
```bash
python test_analytics.py
```
Shows all analytics at once - good for quick overview.

### Interactive demo
```bash
python analytics_demo.py
```
Menu where you can choose what to see.

### Patient management
```bash
python main.py
```
Full CRUD interface for patients.

## What you'll see

### Patient Demographics
- Total patient count: 102
- Age distribution across 5 groups (0-17, 18-29, 30-44, 45-59, 60+)
- Gender split

### Appointment Analysis
- Total appointments: 250
- Status breakdown (Completed, Cancelled, Pending, Confirmed)
- Monthly trends
- Procedure categories

### Peak Hours
- Busiest hour: 12:00 (29 appointments)
- Busiest day: Thursday (185 appointments)
- Hourly and daily distributions

### Revenue Stats
- Total revenue: 275,977 RON
- Average payment: 1,492 RON
- Top procedures by revenue
- Payment methods breakdown

### Doctor Performance
- 10 active doctors
- Appointments per doctor
- Completion rates

## Database info

The SQLite database is in `database/dentalclinic.db` and contains:
- 102 realistic patient records
- 10 doctors with specialties
- 250 appointments over past year
- 185 payment records

All data generated with Faker library using Romanian locale.

## Structure

```
models/       - Patient, Doctor, Appointment classes
repositories/ - Database operations (CRUD)
services/     - Analytics logic
database/     - Database file and generator script
```

## Notes

- Data is fake but realistic (Romanian names/addresses)
- Built while learning Python
- Focus on clean code and analytics features
