# analytics demo - shows different clinic statistics
# trying to make it look good for showing to people

from services.analytics_service import AnalyticsService


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_demographics():
    # show patient demographics
    print_header("PATIENT DEMOGRAPHICS")

    analytics = AnalyticsService()
    demo = analytics.get_patient_demographics()

    if not demo:
        print("No data")
        return

    print(f"\nTotal Patients: {demo['total_patients']}")

    print("\nAge Groups:")
    for age_group, count in sorted(demo['age_groups'].items()):
        percentage = (count / demo['total_patients']) * 100
        print(f"  {age_group:8s}: {count:3d} ({percentage:5.1f}%)")

    print("\nGender:")
    for gender, count in demo['gender'].items():
        percentage = (count / demo['total_patients']) * 100
        print(f"  {gender}: {count} ({percentage:.1f}%)")


def demo_appointments():
    # show appointment statistics
    print_header("APPOINTMENT STATS")

    analytics = AnalyticsService()
    trends = analytics.get_appointment_trends()

    if not trends:
        print("No data")
        return

    print(f"\nTotal Appointments: {trends['total_appointments']}")

    print("\nBy Status:")
    for status, count in sorted(trends['status_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / trends['total_appointments']) * 100
        print(f"  {status:15s}: {count:3d} ({percentage:5.1f}%)")

    print("\nBy Category:")
    for category, count in sorted(trends['category_distribution'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / trends['total_appointments']) * 100
        print(f"  {category:15s}: {count:3d} ({percentage:5.1f}%)")

    print("\nLast 6 Months:")
    monthly = sorted(trends['monthly_trends'].items(), reverse=True)[:6]
    for month, data in reversed(monthly):
        total = data['total']
        completed = data['completed']
        cancelled = data['cancelled']
        completion = (completed / total * 100) if total > 0 else 0
        print(f"  {month}: {total:3d} total, {completed:3d} done, {cancelled:2d} cancelled ({completion:.0f}%)")


def demo_peak_hours():
    # show when clinic is busiest
    print_header("PEAK HOURS")

    analytics = AnalyticsService()
    peak = analytics.get_peak_hours_analysis()

    if not peak:
        print("No data")
        return

    if peak['peak_hour']:
        hour, count = peak['peak_hour']
        print(f"\nBusiest Hour: {hour}:00 with {count} appointments")

    if peak['busiest_day']:
        day, count = peak['busiest_day']
        print(f"Busiest Day: {day} with {count} appointments")

    print("\nAppointments by Hour:")
    for hour in sorted(peak['hourly_distribution'].keys()):
        count = peak['hourly_distribution'][hour]
        print(f"  {hour:02d}:00 - {count} appointments")

    print("\nAppointments by Weekday:")
    # show weekdays in order
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days_order:
        count = peak['weekday_distribution'].get(day, 0)
        if count > 0:
            print(f"  {day:10s}: {count} appointments")


def demo_revenue():
    # show revenue statistics
    print_header("REVENUE ANALYSIS")

    analytics = AnalyticsService()
    revenue = analytics.get_revenue_analysis()

    if not revenue:
        print("No data")
        return

    print(f"\nTotal Revenue: {revenue['total_revenue']:,.2f} RON")
    print(f"Average Payment: {revenue['average_payment']:,.2f} RON")

    print("\nMonthly Revenue (Last 6 Months):")
    monthly = sorted(revenue['monthly_revenue'].items(), reverse=True)[:6]
    for month, amount in reversed(monthly):
        print(f"  {month}: {amount:10,.2f} RON")

    print("\nPayment Methods:")
    for method, count in sorted(revenue['payment_methods'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {method:15s}: {count} payments")

    print("\nTop 5 Revenue Procedures:")
    for i, (procedure, amount) in enumerate(revenue['top_procedures'], 1):
        print(f"  {i}. {procedure:30s}: {amount:10,.2f} RON")


def demo_doctors():
    # show doctor performance
    print_header("DOCTOR PERFORMANCE")

    analytics = AnalyticsService()
    performance = analytics.get_doctor_performance()

    if not performance:
        print("No data")
        return

    print(f"\nActive Doctors: {len(performance)}")
    print("\nPerformance:")
    for doc in performance:
        print(f"  {doc['name']:30s} | {doc['specialty']:20s} | "
              f"{doc['total_appointments']:3d} total | {doc['completed']:3d} done | {doc['completion_rate']:5.1f}%")


def main():
    # main menu for analytics demo
    print("\n" + "=" * 60)
    print("  CLINITRACK - ANALYTICS DASHBOARD")
    print("=" * 60)

    while True:
        print("\n\nChoose what to see:")
        print("  1. Patient Demographics")
        print("  2. Appointment Stats")
        print("  3. Peak Hours")
        print("  4. Revenue Analysis")
        print("  5. Doctor Performance")
        print("  6. Show All")
        print("  0. Exit")

        choice = input("\nYour choice (0-6): ").strip()

        if choice == '1':
            demo_demographics()
        elif choice == '2':
            demo_appointments()
        elif choice == '3':
            demo_peak_hours()
        elif choice == '4':
            demo_revenue()
        elif choice == '5':
            demo_doctors()
        elif choice == '6':
            demo_demographics()
            demo_appointments()
            demo_peak_hours()
            demo_revenue()
            demo_doctors()
        elif choice == '0':
            print("\n" + "=" * 60)
            print("  Thanks for using CliniTrack!")
            print("=" * 60 + "\n")
            break
        else:
            print("\nInvalid choice! Try again.")

        if choice != '0':
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
