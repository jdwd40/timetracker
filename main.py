import datetime
import csv
import string
from collections import defaultdict

# Initialize the log file if it doesn't exist
try:
    open("timetracker.csv", "r")
except FileNotFoundError:
    with open("timetracker.csv", "w", newline='') as csvfile:
        fieldnames = ["date", "task", "duration"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

import string
import datetime
import csv

def add_task():
    task_name = input("\033[97mEnter the task name: \033[0m").strip().translate(str.maketrans('', '', string.digits))
    duration = input("\033[97mEnter the duration (in minutes): \033[0m").strip()

    # Check for empty input
    if not task_name or not duration:
        print("\033[91mInvalid input. Task not added.\033[0m")
        return

    # Check for non-numeric input
    if not duration.isnumeric():
        print("\033[91mInvalid input. Task not added.\033[0m")
        return

    # Check for the existing task name
    existing_task = False
    with open("timetracker.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if task_name.lower() == row[1].lower():
                existing_task = True
                break

    if existing_task:
        confirm_add = input("\033[97mAdd duration to existing task? (y/n): \033[0m").lower()
        if confirm_add != 'y':
            print("\033[91mTask not added.\033[0m")
            return
    else:
        confirm_new = input("\033[97mCreate a new task for today? (y/n): \033[0m").lower()
        if confirm_new != 'y':
            print("\033[91mTask not added.\033[0m")
            return

    # Add the task to the log file
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open("timetracker.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, task_name, duration])

    print(f"\033[92mTask '{task_name}' added successfully.\033[0m")
    list_tasks(1)  # Assuming list_tasks is defined to list today's tasks


def delete_task():
    task_to_delete = input("\033[97mEnter the name of the task to delete: \033[0m").strip()
    rows = []
    task_found = False

    with open("timetracker.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        fields = next(reader)
        for row in reader:
            if len(row) != 3:
                continue

            if row[1] == task_to_delete:
                task_found = True
            else:
                rows.append(row)

    with open("timetracker.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(rows)

    if task_found:
        confirm_delete = input("\033[97mTask found. Delete? (y/n): \033[0m").lower()
        if confirm_delete != 'y':
            print(f"\033[91mTask '{task_to_delete}' not deleted. Returning to main menu.\033[0m")
            return
        print("\033[92mTask deleted successfully.\033[0m")
        list_tasks(0)
    else:
        print(f"\033[91mTask '{task_to_delete}' not found. Returning to main menu.\033[0m")

def list_tasks(days):
    today = datetime.datetime.now().date()
    task_dict = defaultdict(int)
    tasks_found = False 

    with open("timetracker.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) != 3:
                continue
            task_date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
            delta = today - task_date

            if delta.days <= days:
                task_key = f"{row[1]} ({row[0]})"
                task_dict[task_key] += int(row[2])
                tasks_found = True

    print(f"\033[97m{'='*65}\033[0m")
    if days in [0, 7, 30, 999999]:
        time_frames = {0: "Today's", 7: "past 7 days'", 30: "past 30 days'", 999999: "All"}
        print(f"\033[92m{time_frames[days]} Tasks:\033[0m")

    print(f"\033[97m{'Task Name':<30} {'Total Duration (minutes)':<25} {'Date':<10}\033[0m")
    print(f"\033[97m{'='*65}\033[0m")

    for task_key, total_duration in task_dict.items():
        task_name, date = task_key.split(" (")
        date = date.rstrip(")")
        print(f"\033[92m{task_name:<30} {total_duration:<25} {date:<10}\033[0m")
    
    return tasks_found

def list_entries_for_task():
    task_to_list = input("\033[97mEnter the name of the task to list (or 'all' for all tasks): \033[0m").strip()
    task_found = False

    with open("timetracker.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        fields = next(reader)
        
        print(f"\033[97m{'='*65}\033[0m")
        
        if task_to_list.lower() != 'all':
            print(f"\033[92mEntries for Task '{task_to_list}':\033[0m")
        else:
            print(f"\033[92mAll Task Entries:\033[0m")
        
        print(f"\033[97m{'Date':<10} {'Task':<25} {'Duration (minutes)':<25}\033[0m")
        print(f"\033[97m{'='*65}\033[0m")
        
        for row in reader:
            if len(row) != 3:
                continue
            
            if task_to_list.lower() == 'all' or row[1] == task_to_list:
                print(f"\033[92m{row[0]:<10} {row[1]:<25} {row[2]:<25}\033[0m")
                task_found = True

    if not task_found:
        print(f"\033[91mTask '{task_to_list}' not found. Returning to main menu.\033[0m")


def main():
    print(f"\033[97m{'='*65}\033[0m")
    print("\033[92mWelcome to JDTT Time Tracker CLI App!\033[0m")
    # List tasks for today
    print("\033[97mListing tasks for today...\033[0m")
    if not list_tasks(0):  # Assuming list_tasks returns False when no tasks are found for today
        print("\033[93mNo tasks for today yet.\033[0m")

    while True:
        print("\033[97mMenu: A-Add | D-Delete | T-Today | W-7 Days | M-30 Days | E-All | L-List Task | Q-Quit\033[0m")
        choice = input("\033[97mChoice: \033[0m").upper()

        if choice == "A":
            add_task()
        elif choice == "D":
            delete_task()
        elif choice in ["T", "W", "M", "E"]:
            list_tasks({"T": 0, "W": 7, "M": 30, "E": 999999}[choice])
        elif choice == "L":
            list_entries_for_task()
        elif choice == "Q":
            break
        else:
            list_tasks(0)

if __name__ == "__main__":
    main()

