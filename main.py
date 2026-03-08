import tkinter
from tkinter import ttk
from tkinter import messagebox
import os
import openpyxl
import sqlite3
 
 
# Function to view records from the database and display in listbox
def view_records():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
 
    cursor.execute("SELECT * FROM Student_Data")
    records = cursor.fetchall()
 
    conn.close()
 
    # clear existing records in listbox
    records_listbox.delete(0, tkinter.END)
 
    for record in records:
        formatted = f"{record[0]} {record[1]} | {record[2]} | Age: {record[3]} | {record[4]} | Courses: {record[5]} | Semesters: {record[6]} | Status: {record[7]}"
        records_listbox.insert(tkinter.END, formatted)
 
 
def enter_data():
    accepted = accept_var.get()
 
    if accepted=="Accepted":
        #user info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
 
        #checks if user entered the first and last name
        if firstname and lastname:   
            title = title_combobox.get()
            age = age_spinbox.get()
            nationality = nationality_combobox.get()
 
            #course info
            registration_status = reg_status_var.get()
            numcourses = numcourses_spinbox.get()
            numsemesters = numsemesters_spinbox.get()
 
            #printing out all the information
            print("First name: ", firstname, "Last name: ", lastname)
            print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
            print("# Courses: ", numcourses, "# Semesters: ", numsemesters)
            print("Registration Status: ", registration_status)
            print("--------------------------------------------------------")
 
            # SAVING THE INFORMATION IN EXCEL SHEET
            filepath = "data.xlsx"
 
            if not os.path.exists(filepath):
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                heading = ["First Name", "Last Name", "Title", "Age", "Nationality", "# Courses", "# Semesters", "Registration Status"]
                sheet.append(heading)
                workbook.save(filepath)
 
            workbook = openpyxl.load_workbook(filepath)
            sheet = workbook.active
            sheet.append([firstname, lastname, title, age, nationality, numcourses, numsemesters, registration_status])
            workbook.save(filepath)
 
            # SAVING INFORMATION IN SQLITE
            conn = sqlite3.connect('data.db')
 
            table_create_query = """CREATE TABLE IF NOT EXISTS Student_Data (
                firstname TEXT,
                lastname TEXT,
                title TEXT,
                age INT,
                nationality TEXT,
                num_courses INT,
                num_semesters INT,
                registration_status TEXT
            )"""
            conn.execute(table_create_query)
 
            data_insert_query = """INSERT INTO Student_Data (
                firstname, lastname, title, age, nationality,
                num_courses, num_semesters, registration_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
 
            data_insert_tuple = (
                firstname, lastname, title, age, nationality,
                numcourses, numsemesters, registration_status
            )
 
            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)
 
            conn.commit()
            conn.close()
 
        else:
            tkinter.messagebox.showwarning(title="Error!", message="First name and Last name are required.") #error message
    else:
        tkinter.messagebox.showwarning(title= "Error!", message="You have not accepted the terms") #error message
 
 
window = tkinter.Tk()
window.title("Data Entry Form")
 
frame = tkinter.Frame(window)
frame.pack()
 
#saving user info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)
 
first_name_label = tkinter.Label(user_info_frame, text= "First name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text= "Last name")
last_name_label.grid(row=0, column=1)
 
first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)
 
#title for the window
title_label = tkinter.Label(user_info_frame, text="Title")
title_combobox = ttk.Combobox(user_info_frame, values =["Mr.", "Ms.", "Dr."], state="readonly")
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)
 
#age entry
age_label = tkinter.Label(user_info_frame, text="Age")
age_spinbox = tkinter.Spinbox(user_info_frame, from_=18, to=110, state="readonly")
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)
 
#nationality
nationality_label = tkinter.Label(user_info_frame, text="Nationality")
nationality_combobox = ttk.Combobox(user_info_frame, values=["Africa", "Asia", "Antarctica", "Europe","North America", "South America", "Oceania"], state="readonly")
nationality_label.grid(row=2, column=1)
nationality_combobox.grid(row=3, column=1)
 
for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
 
#Saving COurse Info
courses_frame = tkinter.LabelFrame(frame, text="Course Information")
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)
 
registered_label = tkinter.Label(courses_frame, text="Registration Status")
 
reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered", variable=reg_status_var, onvalue="Registered", offvalue="Not registered")
 
registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)
 
numcourses_label = tkinter.Label(courses_frame, text= "# Completed Courses")
numcourses_spinbox = ttk.Spinbox(courses_frame, from_=0, to="infinity")
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)
 
numsemesters_label = tkinter.Label(courses_frame, text="# semesters")
numsemesters_spinbox = ttk.Spinbox(courses_frame, from_=0, to="infinity")
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)
 
for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
 
#terms and conditions
terms_frame = tkinter.LabelFrame(frame, text="Terms and Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)
 
accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="I accept terms and conditions", variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)
 
 
#button to enter data
button = tkinter.Button(frame, text="Enter data", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
 
# button to view records
view_button = tkinter.Button(frame, text="View Records", command=view_records)
view_button.grid(row=4, column=0, sticky="news", padx=20, pady=5)
 
# listbox to display records
records_listbox = tkinter.Listbox(frame, height=8)
records_listbox.grid(row=5, column=0, padx=20, pady=10)
records_listbox.grid(row=5, column=0, sticky="ew", padx=20, pady=10)
 
frame.grid_columnconfigure(0, weight=1)
 
window.mainloop()