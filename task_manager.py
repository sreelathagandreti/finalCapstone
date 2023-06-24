# Capstone project Task Manager
# admin can add users, view all tasks, generate reports and display statistics
# User can add tasks, view tasks, mark tasks as complete

# =====importing libraries===========
import os
from datetime import datetime, date
from typing import List

DATETIME_STRING_FORMAT = "%Y-%m-%d"


# User class to create instances of user
class User:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password


# Task class to create instance of tasks with properties and methods
class Task:
    def __init__(self, username=None, title=None, description=None, due_date=None, assigned_date=None, completed=False):
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    # function used to mark tasks as complete
    def mark_complete(self):
        self.completed = True


# Global variables to store total users as dictionary and tasks as lists
Users_list = {}
Tasks_list: [Task] = []

# current user global variable to store current logged-in user
current_user = {}


# load tasks is a function read the tasks.txt file and store in global variable
def load_tasks():

    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    for t_str in task_data:
        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t = Task(task_components[0], task_components[1], task_components[2],
                      datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
                      datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
                      True if task_components[5] == "Yes" else False)

        Tasks_list.append(curr_t)


# load user function runs to read users details from user.tx file and store in global variable
def load_user():
    """This code reads usernames and password from the user.txt file to
        allow a user to login.
    """

    global Users_list
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        file_data = user_file.read().split("\n")

    # Convert to a dictionary
    for user in file_data:
        username, password = user.split(';')
        Users_list[username] = password


# login function is used to log in functionality
def login():
    global current_user
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in Users_list.keys():
            print("User does not exist")
            continue
        elif Users_list[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            logged_in = True
            print("Login Successful!")
            current_user = User(curr_user, curr_pass)
            return


# function that check if user input have all valid characters
def is_valid_char(input_value):
    if ";" in input_value:
        return False
    else:
        return True


# function used to register new user
def register_user():
    """Add a new user to the user.txt file"""
    # - Request input of a new username
    new_username = input("New Username: ")

    if new_username == '':
        print('Enter a valid username')
        return False

    # - Request input of a new password
    new_password = input("New Password: ")

    if not is_valid_char(new_username) or not is_valid_char(new_password):
        print("Username password should not have invalid ; characters")
        return False

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        Users_list[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in Users_list:
                user_data.append(f"{k};{Users_list[k]}")
            out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        return True
    else:
        print("Passwords do no match")
        return False


# function used to write the latest updated to tasks.txt file to generate reports
def update_tasks():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for task in Tasks_list:
            str_attrs = [
                task.username,
                task.title,
                task.description,
                task.due_date.strftime(DATETIME_STRING_FORMAT),
                task.assigned_date.strftime(DATETIME_STRING_FORMAT),
                "Yes" if task.completed else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


# add task function will add the task to tasks.txt file by taking input from user
def add_task():
    """Allow a user to add a new task to task.txt file
                Prompt a user for the following:
                 - A username of the person whom the task is assigned to,
                 - A title of a task,
                 - A description of the task and
                 - the due date of the task."""
    task_username = input("Name of person assigned to task: ")
    if task_username not in Users_list.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = Task(task_username, task_title, task_description, due_date_time, curr_date, False)

    Tasks_list.append(new_task)
    update_tasks()
    print("Task successfully added.")


# view tasks function will display all tasks or tasks of current user
def view_tasks(all_tasks=False):
    """Reads the task from task.txt file and prints to the console in the
               format of Output 2 presented in the task pdf (i.e. includes spacing
               and labelling)
            """

    for task in Tasks_list:
        if all_tasks or task.username == current_user.username:
            disp_str = f"Task: \t\t\t\t {task.title}\n"
            disp_str += f"Assigned to: \t\t {task.username}\n"
            disp_str += f"Date Assigned: \t\t {task.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t\t {task.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {task.description}\n"
            print(disp_str)

    task_read_response = input('Do you want to mark task as completed? Type Yes or No: ')
    if task_read_response.lower() == 'yes':
        task_name = input('Enter the task title you want to read: ')
        for task in Tasks_list:
            if task_name and task.title.lower() == task_name.lower():
                task.mark_complete()
        update_tasks()

    else:
        print("Returning to main menu")


# function that calculate percentage of given val against the total provided
def calculate_percentage(val, total, round_val=2):
    try:
        if val == 0:
            return 0
        elif val == total:
            return 100
        else:
            return round(val / total * 100, round_val)
    except ZeroDivisionError:
        return 0


# generate reports function called to write reports to user_overview and task_overview files
def generate_reports():
    """
    Generates reports from all the users and tasks
    """
    today_date = datetime.today().strftime(DATETIME_STRING_FORMAT)

    users_overview_str = [
        f"User Overview Report===================================\n",
        f"Total tasks: {len(Tasks_list)}\n"
    ]

    total_completed_tasks = 0
    total_overdue_tasks = 0
    total_number_tasks = len(Tasks_list)

    for user in Users_list:
        user_total_tasks = 0
        user_tasks_complete = 0
        user_tasks_overdue = 0

        for task in Tasks_list:
            if task.username == user:
                user_total_tasks += 1

                if task.completed:
                    user_tasks_complete += 1

                if str(task.due_date) < today_date and not task.completed:
                    user_tasks_overdue += 1

        total_completed_tasks += user_tasks_complete
        total_overdue_tasks += user_tasks_overdue
        user_incomplete_tasks = user_total_tasks - user_tasks_complete

        users_overview_str += [
            f"\n{user} Report\n",
            f"Total Tasks\t\t\t\t\t\t\t\t {user_total_tasks}\n",
            f"Percentage of Total number of tasks\t\t {calculate_percentage(user_total_tasks, total_number_tasks)} \n"
            f"Percentage of completed tasks\t\t\t {calculate_percentage(user_tasks_complete, user_total_tasks)}\n",
            f"Percentage of incomplete tasks\t\t\t {calculate_percentage(user_incomplete_tasks, user_total_tasks)}\n",
            f"Percentage of overdue tasks\t\t\t\t {calculate_percentage(user_tasks_overdue, user_total_tasks)}\n",
            f"===================================\n"
        ]

    total_incomplete_tasks = total_number_tasks - total_completed_tasks

    tasks_str_out = [
        f"Tasks Report=========================\n",
        f"Total number of tasks\t\t\t\t\t\t {total_number_tasks}\n"
        f"Total number of completed tasks \t\t\t {total_completed_tasks}\n"
        f"Total number of incomplete tasks \t\t\t {total_incomplete_tasks}\n"
        f"Total number of overdue tasks \t\t\t\t {total_overdue_tasks}\n"
        f"Percentage of tasks incomplete\t\t\t\t {calculate_percentage(total_incomplete_tasks, total_number_tasks)}\n"
        f"Percentage of tasks overdue\t\t\t\t\t {calculate_percentage(total_overdue_tasks, total_number_tasks)}\n"
    ]

    with open('task_overview.txt', 'w') as task_overview_file:
        for val in tasks_str_out:
            task_overview_file.write(val)

    with open('user_overview.txt', 'w') as user_overview_file:
        for val in users_overview_str:
            user_overview_file.write(val)
    print('New Report has been generated!!')


# Run default functions
load_user()
load_tasks()
login()

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    if current_user.username == 'admin':
        menu = input('''Select one of the following Options below:
           r - Registering a user
           a - Adding a task
           va - View all tasks
           vm - View my task
           ds - Display statistics
           gr - generate reports
           e - Exit
           : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
       a - Adding a task
       va - View all tasks
       vm - View my task
       e - Exit
       : ''').lower()

    if menu == 'r':
        if current_user.username != 'admin':
            print('Registering new users is not allowed, please contact admin')
            continue

        if not register_user():
            continue

    elif menu == 'a':
        # if user successfully added task to task list
        add_task()
        continue

    elif menu == 'va':  # View all tasks
        view_tasks(True)

    elif menu == 'vm':
        view_tasks(False)

    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds' and current_user.username == 'admin':
        generate_reports()
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''

        if not os.path.exists('task_overview.txt') or not os.path.exists('user_overview.txt'):
            print('Failed to find data source to print reports')
            continue

        else:
            num_users = len(Users_list.keys())
            num_tasks = len(Tasks_list)

            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")

            with open('user_overview.txt') as user_overview:
                for line in user_overview:
                    print(line, end="")

            with open('task_overview.txt') as task_overview:
                for line in task_overview:
                    print(line, end="")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
