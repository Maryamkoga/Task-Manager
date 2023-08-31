# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.


import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8"):
        pass
username_password = {}

def reg_user():
    '''Add a new user to the user.txt file'''
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        with open("user.txt", "r", encoding="utf-8") as user_file:
            existing_usernames = [line.split(";")[0] for line in user_file.read().split("\n")]

        if new_username in existing_usernames:
            print("Username already exists. Please choose a different username.")
        else:
            with open("user.txt", "a", encoding="utf-8") as user_file:
                user_file.write(f"\n{new_username};{new_password}")
            # Update the username_password dictionary
            username_password[new_username] = new_password
            print("New user added")
    else:
        print("Passwords do not match")


def add_task():
    #Prompts the user to enter the username assigned to the task 
    task_username = input("Name of person assigned to task: ")
    #Checks if the username entered exists in the  dictionary 
    #Prints and error message if not 
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return
    #Prompts the user to enter necessary details for the task 
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date,
        "assigned_date": curr_date,
        "completed": False
    }
    #Tasks added are appended to the task list 
    task_list.append(new_task)
    with open("tasks.txt", "a", encoding="utf-8") as new_task_file:
        new_task_file.write(f"{new_task['username']};{new_task['title']};{new_task['description']};{new_task['due_date'].strftime(DATETIME_STRING_FORMAT)};{new_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{new_task['completed']}\n")
    print("Task successfully added.")

def view_all():
    #View all tasks from tasks.txt
    with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
        tasks = tasks_file.readlines()
    #To read all tasks in tasks.txt and print them when selected as an option
    print("\nAll Tasks:")
    if tasks:
        for task in tasks:
            task_details = task.strip().split(";")
            print(f"Assigned to: {task_details[0]}")
            print(f"Title: {task_details[1]}")
            print(f"Description: {task_details[2]}")
            print(f"Due Date: {task_details[3]}")
            print(f"Assigned Date: {task_details[4]}")
            print(f"Completed: {task_details[5]}")
            print("------------------------------------")

def view_mine():
    '''Display tasks assigned to the logged-in user'''
    current_user = input("Enter your username: ")

    my_tasks = [task for task in task_list if task["username"] == current_user]
    #To print taksks assigned to current user with task numbers 
    print(f"\nTasks Assigned to {current_user}:")
    if my_tasks:
        for i, task in enumerate(my_tasks, start=1):
            print(f"Task {i}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print("------------------------------------")
    else:
        print("No tasks found for the user")
    #User is provided with options to edit tasks, mark them as complete or return to the main menu 
    print("\nSelect a task number to edit, or enter '-1' to return to the main menu.")
    selected_task = input("Choice: ")

    if selected_task == "-1":
        return

    selected_task = int(selected_task)

    if selected_task < 1 or selected_task > len(my_tasks):
        print("Invalid task number.")
        return

    task_to_edit = my_tasks[selected_task - 1]
    task_description = task_to_edit["description"]
    task_assigned_to = task_to_edit["username"]
    task_due_date = str(task_to_edit["due_date"])
    # Check if the task is already marked as complete
    if task_to_edit['completed']:
        print("This task has already been marked as complete and cannot be edited.")
        return
    #Print details of task to be edited 
    print("\nTask Details:")
    print("-------------")
    print(f"Description: {task_description}")
    print(f"Assigned to: {task_assigned_to}")
    print(f"Due date: {task_due_date}")
    #Menu that displays options to user 
    print("\nWhat would you like to do?")
    print("1. Mark task as complete")
    print("2. Edit task")
    print("3. Return to the main menu")
    choice = input("Choice: ")

    if choice == "1":
        mark_task_complete(selected_task)
    elif choice == "2":
        edit_task(selected_task, task_description, task_assigned_to, task_due_date)
    elif choice == "3":
        return
    else:
        print("Invalid choice.")


def mark_task_complete(task_index):
    '''Mark a task as complete'''
    with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
        tasks = tasks_file.readlines()

    task_to_mark = tasks[task_index - 1].strip()

    if "Yes" in task_to_mark:
        print("This task is already marked as complete.")
        return

    tasks[task_index - 1] = task_to_mark.replace("No", "Yes")

    with open("tasks.txt", "w", encoding="utf-8") as tasks_file:
        tasks_file.writelines(tasks)

    print("Task marked as complete.")


def edit_task(task_index, task_description, task_assigned_to, task_due_date):
    '''Edit a task'''
    #The user enters the new details for the selected task 
    new_description = input("New Description: ")
    new_assigned_to = input("New Assigned to: ")
    new_due_date = input("New Due Date (YYYY-MM-DD): ")

    tasks = []
    with open("tasks.txt", "r", encoding="utf-8") as tasks_file:
        tasks = tasks_file.readlines()
    #The taask.txt file is updated with the new information 
    task_to_edit = tasks[task_index - 1].strip()
    tasks[task_index - 1] = task_to_edit.replace(
        f"{task_description};{task_assigned_to};{task_due_date}", f"{new_description};{new_assigned_to};{new_due_date}"
    )

    with open("tasks.txt", "w", encoding="utf-8") as tasks_file:
        tasks_file.writelines(tasks)
    #Print statement to acknowledge task has been updated 
    print("Task updated.")

# Function to display statistics from text files
def display_statistics():
    '''If the user is an admin they can display statistics about number of users
        and tasks.'''
     # Check if the text files exist
    try:
        # Read and display the contents of "tasks.txt"
        print("Tasks Overview")
        print("================")
        with open("tasks.txt", "r", encoding= "utf-8") as tasks_file:
            tasks_content = tasks_file.read()
            print(tasks_content)
    except FileNotFoundError:
        print("Text files not found. Please generate them first.")
    
    try:
        # Read and display the contents of "users.txt"
        print("\nUsers Overview")
        print("================")
        with open("user.txt", "r", encoding= "utf-8") as users_file:
            users_content = users_file.read()
            print(users_content)
    except FileNotFoundError:
        print("Text files not found. Please generate them first.")

def overdue(task):
     # Checks if the task is overdue
    if task.completed:
        return False
    return task.due_date < date.today()


def generate_reports(tasks, users):
    #Try/except statement to catch any zero division errors 
    try:
        # Generate task_overview.txt
        with open("task_overview.txt", "w", encoding="utf-8") as report_file:
            #Variables to calculate necessary information that will go in new text files created
            total_tasks = len(tasks)
            completed_tasks = sum(task.completed for task in tasks)
            uncompleted_tasks = total_tasks - completed_tasks
            overdue_tasks = sum(task.overdue() for task in tasks)
            #If statement is added to return a value of 0% instead of the error statement 
            incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 
            overdue_percentage = (overdue_tasks / total_tasks) * 100 

            #To write the results to new text file 
            report_file.write("Task Overview\n")
            report_file.write("================\n")
            report_file.write(f"Total tasks generated and tracked: {total_tasks}\n")
            report_file.write(f"Completed tasks: {completed_tasks}\n")
            report_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
            report_file.write(f"Overdue tasks: {overdue_tasks}\n")
            report_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
            report_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")
            report_file.write("================\n")

        # Generate user_overview.txt
        with open("user_overview.txt", "w", encoding="utf-8") as user_file:
            total_users = len(users)

            user_file.write("\nUser Overview\n")
            user_file.write("================\n")
            user_file.write(f"Total users registered with task_manager.py: {total_users}\n")

            for user in users:
                assigned_tasks = sum(user == task.username for task in tasks)
                completed_assigned_tasks = sum(user == task.username and task.completed for task in tasks)
                incomplete_assigned_tasks = assigned_tasks - completed_assigned_tasks
                #If statement is added to return a value of 0% instead of the zero division error statement 
                incomplete_percentage = (incomplete_assigned_tasks / assigned_tasks) * 100 
                overdue_assigned_tasks = sum(user == task.username and task.overdue() for task in tasks)
                overdue_percentage = (overdue_assigned_tasks / assigned_tasks) * 100 
                
                #To write the results to new text file
                user_file.write(f"\nUser: {user}\n")
                user_file.write(f"Total tasks assigned: {assigned_tasks}\n")
                user_file.write(f"Percentage of assigned tasks completed: {completed_assigned_tasks / assigned_tasks:.2f}%\n")
                user_file.write(f"Percentage of assigned tasks incomplete: {incomplete_percentage:.2f}%\n")
                user_file.write(f"Percentage of assigned tasks overdue: {overdue_percentage:.2f}%\n")
                user_file.write("================\n")
    #To catch zero division error 
    except ZeroDivisionError:
        print("No tasks present in task.txt file")


def login():
    #The user.txt file that contains username-password is accessed 
    with open("user.txt", "r", encoding="utf-8") as user_file:
        user_data = user_file.read().split("\n")

    #Clear the existing data in the username_password dictionary
    username_password.clear()

    for user in user_data:
        values = user.split(';')
        if len(values) == 2:
            username, password = values 
            username_password[username] = password
        else:
            #To handle the case where there aren't exactly two values
            print("Ignoring invalid user data!")
    

    #User login 
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password:
            print("User does not exist")
            register_option = input("Do you want to register? (Y/N): ")
            if register_option.upper() == "Y":
                reg_user()
            elif register_option.upper() == "N":
                exit()
            else:
                print("Invalid input, try again")
                continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong username or password")
            continue
        elif curr_user == "admin" and curr_pass == username_password[curr_user]:
            print("Admin login successful!")
            logged_in = True
        else:
            print("Login Successful!")
            logged_in = True

# Read tasks from tasks.txt file
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    task_components = t_str.split(";")
    if len(task_components) >= 6:
        curr_t = {}
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)

def start():
    # Main program loop
    logged_in = False
    is_admin = False 
    while not logged_in:
        curr_user = "admin"
        if login():
            #Code to be executed after succesful login
            print("Welcome!")
            logged_in = True
        if curr_user == "admin":
            is_admin = True

        #To print menu option for user to pick from
        print("\n===== Task Manager =====")
        print("Menu:")
        print("r - Register a User")
        print("a - Add a Task")
        print("va - View All Tasks")
        print("vm - View My Tasks")
        #Additional admin options
        if is_admin:
            print("gr - Generate Reports")
            print("ds - Display Statistics")
        print("e - Exit")

        out_tasks = []
        out_users = []
        
        #Input to accept user choice 
        menu = input("Enter your choice: ")
        #Statements to generate results based on user option 
        if menu == 'r':
            reg_user()
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all()
        elif menu == 'vm':
            view_mine()
        elif is_admin and menu == 'gr':
            generate_reports(out_tasks, out_users)
        elif is_admin and menu == 'ds':
            display_statistics()
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice. Please try again")
    # Login the user
start()
