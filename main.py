
import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def enter_data():
    accepted = accept_var.get()

    if accepted == "Accepted":
        firstname = first_name_entry.get().strip()
        lastname = last_name_entry.get().strip()
        fullname = firstname + " " + lastname

        if firstname and lastname: 
            title = title_combobox.get()
            age = age_spinbox.get()
            nationality = nationality_combobox.get()
            registration_status = reg_status_var.get()
            numcourses = num_courses_spinbox.get()
            numsemesters = num_semesters_spinbox.get()

            print("First name: ", firstname)
            print("Last name:", lastname)
            print("Full name: ", fullname)
            print("Title: ", title)
            print("Age: ", age)
            print("Nationality: ", nationality)
            print("# Courses: ", numcourses)
            print("# Semesters: ", numsemesters)
            print("Registration status", registration_status)
            print("-------------------------------------------------")

            messagebox.showinfo(title="Success", message="Data entered successfully!")

            # Create Table 

            # Create Table
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            table_create_query = '''CREATE TABLE IF NOT EXISTS Students_Data 
            ( firstname TEXT, lastname TEXT,fullname TEXT, title TEXT, age INT, nationality TEXT,
            registration_status TEXT, numcourses INT, numsemesters INT )
            '''
            cursor.execute(table_create_query)

           # insert data 
            data_insert_query = ''' INSERT INTO Students_Data (firstname, lastname, fullname, title,
           age, nationality, registration_status, numcourses, numsemesters ) VALUES  
           (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            data_insert_tuple = (firstname, lastname, fullname, title, 
                                 age, nationality, registration_status, numcourses, numsemesters)
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()


        else: 
            tkinter.messagebox.showwarning(title="Error", message="First name and Last name are required")

    else: 
        tkinter.messagebox.showwarning(title="Error", message="You have not accepted the terms")

# New function to view records
def view_records():
    view_window = tkinter.Toplevel(window)
    view_window.title("View Student Records" )
    view_window.geometry("800x400")

    # Create Treeview widget
    tree = ttk.Treeview(view_window, 
                        columns=("First Name", "Last Name", "Full Name", "Title", 
                                "Age", "Nationality", "Registration Status", 
                                "# Courses", "# Semesters"),
                        show="headings")

    # Define column headings
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Full Name", text="Full Name")
    tree.heading("Title", text="Title")
    tree.heading("Age", text="Age")
    tree.heading("Nationality", text="Nationality")
    tree.heading("Registration Status", text="Registration Status")
    tree.heading("# Courses", text="# Courses")
    tree.heading("# Semesters", text="# Semesters")

    tree.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

    # Fetch data from database
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students_Data")
        records = cursor.fetchall()

        # Insert records into treeview
        for record in records:
            tree.insert("", tkinter.END, values=record)

        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error reading database: {str(e)}")

    # Button to close window
    close_button = tkinter.Button(view_window, text="Close", command=view_window.destroy,
                                 bg="red", fg="black", font=("Arial", 12))
    close_button.pack(pady=10)

window = tkinter.Tk()
window.title("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()

user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0, padx=5, pady=5)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1, padx=5, pady=5)
title_label = tkinter.Label(user_info_frame, text="Title")
title_label.grid(row=0, column=2, padx=5, pady=5)

first_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry = tkinter.Entry(user_info_frame)
last_name_entry.grid(row=1, column=1)
title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr."])
title_combobox.grid(row=1, column=2)

age_label = tkinter.Label(user_info_frame, text="Age")
age_label.grid(row=2, column=0)
nationality_label = tkinter.Label(user_info_frame, text="Nationality")
nationality_label.grid(row=2, column=1)

age_spinbox = tkinter.Spinbox(user_info_frame, from_=18, to=110)
age_spinbox.grid(row=3, column=0)
nationality_combobox = ttk.Combobox(user_info_frame, values=["China", "Egypt", "Palestine", "Jordan", "Syria"])
nationality_combobox.grid(row=3, column=1)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

courses_frame = tkinter.LabelFrame(frame, text="Course Information")
courses_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

registered_label = tkinter.Label(courses_frame, text="Registration Status")
registered_label.grid(row=0, column=0)

reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not Registered")
registered_check.grid(row=1, column=0)

num_courses_label = tkinter.Label(courses_frame, text="# Completed Courses")
num_courses_label.grid(row=0, column=1)
num_courses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to=100)
num_courses_spinbox.grid(row=1, column=1)

num_semesters_label = tkinter.Label(courses_frame, text="# Semesters")
num_semesters_label.grid(row=0, column=2)
num_semesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to=20)
num_semesters_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions", 
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0, padx=5, pady=5)

# Button frame to hold both buttons
button_frame = tkinter.Frame(frame)
button_frame.grid(row=3, column=0, padx=20, pady=20)

# Enter Data button
enter_button = tkinter.Button(button_frame, text="Enter Data", command=enter_data, 
                             bg="lightgreen", fg="black", font=("Arial", 12))
enter_button.pack(side=tkinter.LEFT, padx=10)

# View Records button (new feature)
view_button = tkinter.Button(button_frame, text="View Records", command=view_records, 
                            bg="yellow", fg="black", font=("Arial", 12))
view_button.pack(side=tkinter.LEFT, padx=10)

window.mainloop()

 
