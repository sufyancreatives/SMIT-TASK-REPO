import os

FILE_NAME = "students.txt"

# This function checks if the entered student information is correct or not.
def validate_student(student_Data):
    roll = student_Data["ROLL NUMBER"]
    name = student_Data["NAME"]
    age = student_Data["AGE"]
    grade = student_Data["GRADE"]
    marks = student_Data["MARKS"]

    # Making sure roll number is a number
    if not str(roll).isdigit():
        print("Error: Roll number must be numeric.")
        return False

    # Checking if roll number already exists in file
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            for line in f:
                existing_id = line.strip().split(',')[0]
                if str(roll) == existing_id:
                    print("Error: Roll number already exists.")
                    return False

    # Name should only have alphabets and spaces
    if not name.replace(" ", "").isalpha():
        print("Error: Name must only contain letters.")
        return False

    # Age should be a positive number
    if not str(age).isdigit() or int(age) <= 0:
        print("Error: Age must be a positive number.")
        return False

    # Grade should be A–F only and in uppercase
    if not grade.isalpha() or len(grade) != 1 or not grade.isupper() or grade > "F":
        print("Error: Grade must be a single uppercase letter (A–F).")
        return False

    # Marks should be between 0 and 100
    if not str(marks).isdigit() or not (0 <= int(marks) <= 100):
        print("Error: Marks must be between 0 and 100.")
        return False

    # If everything is fine, return True
    return True


# This function saves a single student's data into the text file.
def save_student(student_Data):
    with open(FILE_NAME, 'a') as f:
        f.write(f"{student_Data['ROLL NUMBER']},{student_Data['NAME']},{student_Data['AGE']},{student_Data['GRADE']},{student_Data['MARKS']}\n")


# This function reads all students' data from the file and returns them in a list.
def read_students():
    students = []
    if not os.path.exists(FILE_NAME):
        return students
    with open(FILE_NAME, 'r') as f:
        for line in f:
            data = line.strip().split(',')
            if len(data) == 5:
                students.append({
                    "ROLL NUMBER": data[0],
                    "NAME": data[1],
                    "AGE": data[2],
                    "GRADE": data[3],
                    "MARKS": data[4]
                })
    return students


# This function overwrites the file with the updated list of students.
def write_students(students):
    with open(FILE_NAME, 'w') as f:
        for s in students:
            f.write(f"{s['ROLL NUMBER']},{s['NAME']},{s['AGE']},{s['GRADE']},{s['MARKS']}\n")


# This function allows the user to enter new student details from the keyboard.
def add_student():
    student_Data = {}
    student_Data["ROLL NUMBER"] = int(input("ENTER YOUR ROLL NUMBER OR STUDENT ID: "))
    student_Data["NAME"] = input("ENTER YOUR NAME: ")
    student_Data["AGE"] = int(input("ENTER YOUR AGE: "))
    student_Data["GRADE"] = input("ENTER YOUR GRADE (A–F): ").upper()
    student_Data["MARKS"] = int(input("ENTER YOUR MARKS OUT OF 100: "))

    # Before saving, check if the data is valid
    if validate_student(student_Data):
        save_student(student_Data)
        print("Student added successfuslly!")
    else:
        print("Student not saved due to invalid input.")


# This function prints all students' data on the screen.
def view_students():
    students = read_students()
    if not students:
        print("No records found.")
        return
    print("\nALL STUDENTS DATA\n")
    for s in students:
        print(f"ROLL NUMBER: {s['ROLL NUMBER']}, NAME: {s['NAME']}, AGE: {s['AGE']}, GRADE: {s['GRADE']}, MARKS: {s['MARKS']}")
    print(f"Total Students: {len(students)}")


# This function helps you find a student by name or roll number.
def search_student():
    students = read_students()
    if not students:
        print("No records found.")
        return
    query = (input("ENTER STUDENT NAME TO SEARCH: "))
    found = [s for s in students if s["ROLL NUMBER"] == query or query in s["NAME"]]
    if not found:
        print("This student is not found in data.")
    else:
        for s in found:
            print(f"ROLL NUMBER: {s['ROLL NUMBER']}, NAME: {s['NAME']}, AGE: {s['AGE']}, GRADE: {s['GRADE']}, MARKS: {s['MARKS']}")


# This function updates an existing student's record using their roll number.
def update_student():
    students = read_students()
    if not students:
        print("No records found.")
        return
    id_ = input("Enter Student Roll Number to update: ").strip()
    found = False
    for s in students:
        if s["ROLL NUMBER"] == id_:
            found = True
            print(f"Current Record: {s}")
            # Ask user which fields they want to change
            new_name = input("Enter new name (leave blank to keep same): ").strip()
            new_age = input("Enter new age (leave blank to keep same): ").strip()
            new_grade = input("Enter new grade (leave blank to keep same): ").strip().upper()
            new_marks = input("Enter new marks (leave blank to keep same): ").strip()
            # Only change fields if user enters something
            if new_name:
                s["NAME"] = new_name
            if new_age and new_age.isdigit():
                s["AGE"] = new_age
            if new_grade:
                s["GRADE"] = new_grade
            if new_marks and new_marks.isdigit():
                s["MARKS"] = new_marks
            break
    if found:
        write_students(students)
        print("Record updated successfully.")
    else:
        print("Student Roll Number not found.")


# This function deletes a student's record from the file.
def delete_student():
    students = read_students()
    if not students:
        print("No records found.")
        return
    id_ = input("Enter Student Roll Number to delete: ").strip()
    new_list = [s for s in students if s["ROLL NUMBER"] != id_]
    if len(new_list) == len(students):
        print("No such student found.")
        return
    confirm = input("Are you sure you want to delete this student? (yes/no): ").lower()
    if confirm == "yes":
        write_students(new_list)
        print("Student data has been deleted.")
    else:
        print("Deletion cancelled.")


# This function calculates average marks, top performer, and lowest marks.
def analyze_data():
    students = read_students()
    if not students:
        print("No data to analyze.")
        return
    marks = [int(s["MARKS"]) for s in students]
    total_marks = sum(marks)
    average = total_marks / len(marks)
    highest_marks = max(marks)
    lowest_marks = min(marks)
    top_performer = [s["NAME"] for s in students if int(s["MARKS"]) == highest_marks][0]
    below_average = [s for s in students if int(s["MARKS"]) < average]
    print("--- Data Analysis ---")
    print(f"Average Marks: {average:.2f}")
    print(f"Top Performer: {top_performer} ({highest_marks})")
    print(f"Students Below Average: {len(below_average)}")
    print(f"Highest Marks: {highest_marks} | Lowest: {lowest_marks}")


# This is the main menu of the program.
# It keeps running until the user decides to exit.
def main():
    while True:
        print("\n====== Smart Student Record Analyzer ======")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Analyze Data")
        print("7. Exit")
        choice = input("Enter your choice: ")

        # Based on user’s choice, perform the matching action
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            analyze_data()
        elif choice == "7":
            print("Thank you for using Smart Student Record Analyzer.")
            break
        else:
            print("Invalid choice, please try again.")


# Start the program by calling main()
main()
