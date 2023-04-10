import datetime
import schedule
import time

def create_reminder():
    """
    Prompts the user to create a new reminder and schedules it to run at the specified time.
    """
    reminder_text = input("Enter reminder: ")
    reminder_time_str = input("Enter reminder time (YYYY-MM-DD HH:MM:SS): ")
    try:
        reminder_time = datetime.datetime.strptime(reminder_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print("Error: Invalid time format. Use 'YYYY-MM-DD HH:MM:SS'.")
        return

    def generate_reminder():
        print(f"Reminder: {reminder_text}")

    schedule.every().day.at(reminder_time.strftime("%H:%M")).do(generate_reminder)

    print("Reminder created successfully!")
    
while True:
    create_or_exit = input("Enter 'c' to create a reminder, or 's' to stop the program: ")
    if create_or_exit == 'c':
        create_reminder()
    elif create_or_exit == 's':
        break
    else:
        print("Invalid input. Please enter 'c' or 's'.")

    time.sleep(1)
    schedule.run_pending()
