# quick test to see if analytics work
# just runs all the analytics functions and shows output

from services.analytics_service import AnalyticsService


def main():
    print("\nCLINITRACK - ANALYTICS TEST")
    print("=" * 60)

    analytics = AnalyticsService()

    # test demographics
    print("\n1. Patient Demographics")
    print("-" * 60)
    demo = analytics.get_patient_demographics()
    print(f"Total Patients: {demo['total_patients']}")
    print(f"Age Groups: {demo['age_groups']}")
    print(f"Gender: {demo['gender']}")

    # test appointments
    print("\n2. Appointment Trends")
    print("-" * 60)
    trends = analytics.get_appointment_trends()
    print(f"Total Appointments: {trends['total_appointments']}")
    print(f"Status: {trends['status_distribution']}")
    print(f"Categories: {trends['category_distribution']}")

    # test peak hours
    print("\n3. Peak Hours")
    print("-" * 60)
    peak = analytics.get_peak_hours_analysis()
    if peak['peak_hour']:
        hour, count = peak['peak_hour']
        print(f"Peak Hour: {hour}:00 ({count} appointments)")
    if peak['busiest_day']:
        day, count = peak['busiest_day']
        print(f"Busiest Day: {day} ({count} appointments)")

    # test revenue
    print("\n4. Revenue")
    print("-" * 60)
    revenue = analytics.get_revenue_analysis()
    print(f"Total Revenue: {revenue['total_revenue']:,.2f} RON")
    print(f"Average Payment: {revenue['average_payment']:,.2f} RON")
    print(f"Payment Methods: {revenue['payment_methods']}")
    print("\nTop 5 Procedures:")
    for i, (proc, amount) in enumerate(revenue['top_procedures'], 1):
        print(f"  {i}. {proc}: {amount:,.2f} RON")

    # test doctor performance
    print("\n5. Doctor Performance")
    print("-" * 60)
    doctors = analytics.get_doctor_performance()
    print(f"Active Doctors: {len(doctors)}")
    for doc in doctors[:5]:
        print(f"  {doc['name']}: {doc['total_appointments']} appointments, {doc['completion_rate']:.1f}% done")

    print("\n" + "=" * 60)
    print("All tests done!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
