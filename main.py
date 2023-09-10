# Time Tracker CLI App Documentation Overview
#
# The Time Tracker is a command-line application developed in Python. Upon launch, it displays a menu with several options for task management and reporting:
#
# - **A**: Add a new task along with its duration.
# - **D**: Delete an existing task.
# - **T**: Display all tasks and their durations for today.
# - **W**: List all tasks and durations for the past 7 days.
# - **M**: List all tasks and durations for the past 30 days.
# - **E**: List all tasks and durations stored in the log file.
#
# The user can select an option by typing its corresponding letter. For adding tasks, the application prompts for the task name and its duration. All task-related data is stored in a # log file, which the application reads from to display task lists as per the user's request.

# 1. Initialize the Log File
# First, check if the log file exists. If not, create a new CSV file and write the header.

import datetime
import csv

# Initialize the log file if it doesn't exist
try:
    open("timetracker.csv", "r")
except FileNotFoundError:
    with open("timetracker.csv", "w", newline='') as csvfile:
        fieldnames = ["date", "task", "duration"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def add_task():
    ## promt the user for the task name and duration
    task_name = input("Enter the task name: ").strip()
    duration = input("Enter the duration (in minutes): ").strip()

    ## check for empty input
    if not task_name or not duration:
        print("Invalid input. Task not added.")
        return
    
    ## check for non-numeric input
    if not duration.isnumeric():
        print("Invalid input. Task not added.")
        return
    
    ## add the task to the log file
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    with open("timetracker.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, task_name, duration])

    ## provide feedback to the user
    print(f"Task '{task_name}' added successfully.")

# show tasks for today
    list_tasks(1) 

def delete_task():
    task_to_delete = input("Enter the name of the task to delete: ").strip()
    rows = []
    task_found = False  # Flag to check if the task exists

    # Read the log file and store all rows except the one to be deleted
    with open("timetracker.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        fields = next(reader)  # Skip the header
        for row in reader:
            # Skip any rows that don't contain the expected number of elements
            if len(row) != 3:
                continue

            if row[1] == task_to_delete:
                task_found = True  # Task exists
            else:
                rows.append(row)
                
    # Write the updated rows back to the log file
    with open("timetracker.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(rows)

    # Provide user feedback
    if task_found:
        print("Task deleted successfully.")
        print("Here are your tasks for today:")
        list_tasks(0)  # List tasks for today
    else:
        print(f"Task '{task_to_delete}' not found. Returning to main menu.")


from collections import defaultdict

# Task 3.3: List Tasks
def list_tasks(days):
    today = datetime.datetime.now().date()
    task_dict = defaultdict(int)  # A dictionary to store the total duration for each task
    
    # Read the log file and populate the task_dict
    with open("timetracker.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            # Skip any rows that don't contain the expected number of elements
            if len(row) != 3:
                continue
            task_date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
            delta = today - task_date
            
            if delta.days <= days:
                task_key = f"{row[1]} ({row[0]})"  # Create a key like "task_name (date)"
                task_dict[task_key] += int(row[2])  # Sum up the total duration for each task
                
    # Print the tasks in a cleaner format
    print(f"{'Task Name':<30} {'Total Duration (minutes)':<25} {'Date':<10}")
    print("="*65)
    for task_key, total_duration in task_dict.items():
        task_name, date = task_key.split(" (")
        date = date.rstrip(")")
        print(f"{task_name:<30} {total_duration:<25} {date:<10}")


def main():
    while True:
        # Display the menu options on a single line
        print("Menu: A-Add | D-Delete | T-Today | W-7 Days | M-30 Days | E-All | Q-Quit")
        
        # Get user choice
        choice = input("Choice: ").upper()
        
        if choice == "A":
            add_task()
        elif choice == "D":
            delete_task()
        elif choice == "T":
            list_tasks(0)
        elif choice == "W":
            list_tasks(7)
        elif choice == "M":
            list_tasks(30)
        elif choice == "E":
            list_tasks(999999)  # List all tasks
        elif choice == "Q":
            break
        else:
            list_tasks(1)  # List tasks for today

if __name__ == "__main__":
    main()



