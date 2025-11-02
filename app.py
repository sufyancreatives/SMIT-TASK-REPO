import streamlit as st
import os

FILE_NAME = "students.txt"

def validate_input(id_, name, age, grade, marks, check_unique=True):
    if not str(id_).isdigit():
        return False, "ID must be an integer"
    if check_unique:
        students = read_students()
        for s in students:
            if s['id_'] == str(id_):
                return False, "ID already exists"
    if not name.strip() or any(ch.isdigit() for ch in name):
        return False, "Name must be alphabetic"
    if not str(age).isdigit() or int(age) <= 0:
        return False, "Age must be positive"
    if grade.upper() not in ['A','B','C','D','E','F']:
        return False, "Grade must be between A-F"
    if not str(marks).isdigit() or not (0 <= int(marks) <= 100):
        return False, "Marks must be between 0 and 100"
    return True, ""

def read_students():
    students = []
    if not os.path.exists(FILE_NAME):
        return students
    with open(FILE_NAME, "r") as f:
        for line in f:
            data = line.strip().split(",")
            if len(data) == 5:
                id_, name, age, grade, marks = data
                students.append({
                    "id_": id_,
                    "name": name,
                    "age": int(age),
                    "grade": grade,
                    "marks": int(marks)
                })
    return students

def write_students(students):
    with open(FILE_NAME, "w") as f:
        for s in students:
            f.write(f"{s['id_']},{s['name']},{s['age']},{s['grade']},{s['marks']}\n")

def add_student(id_, name, age, grade, marks):
    ok, msg = validate_input(id_, name, age, grade, marks)
    if not ok:
        return False, msg
    students = read_students()
    students.append({
        "id_": str(id_),
        "name": name,
        "age": int(age),
        "grade": grade.upper(),
        "marks": int(marks)
    })
    write_students(students)
    return True, "Student added successfully"

def update_student(id_, name, age, grade, marks):
    students = read_students()
    found = False
    for s in students:
        if s['id_'] == str(id_):
            found = True
            ok, msg = validate_input(id_, name, age, grade, marks, check_unique=False)
            if not ok:
                return False, msg
            s['name'] = name
            s['age'] = int(age)
            s['grade'] = grade.upper()
            s['marks'] = int(marks)
            break
    if not found:
        return False, "ID not found"
    write_students(students)
    return True, "Record updated"

def delete_student(id_):
    students = read_students()
    new_list = [s for s in students if s['id_'] != str(id_)]
    if len(new_list) == len(students):
        return False, "ID not found"
    write_students(new_list)
    return True, "Record deleted"

def analyze_data():
    students = read_students()
    if not students:
        return None
    marks_list = [s['marks'] for s in students]
    total = sum(marks_list)
    average = total / len(students)
    highest = max(marks_list)
    lowest = min(marks_list)
    below_avg = [s for s in students if s['marks'] < average]
    top_student = [s for s in students if s['marks'] == highest]
    pass_count = len([s for s in students if s['marks'] >= 40])
    fail_count = len(students) - pass_count
    return {
        "total": total,
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "below_count": len(below_avg),
        "top": top_student,
        "pass_count": pass_count,
        "fail_count": fail_count
    }

st.title("Smart Student Record Analyzer")

menu = st.sidebar.selectbox("Menu", ["Add Student", "View Students", "Search Student", "Update Student", "Delete Student", "Analyze Data"])

if menu == "Add Student":
    st.header("Add Student Record")
    id_ = st.text_input("Enter ID")
    name = st.text_input("Enter Name")
    age = st.text_input("Enter Age")
    grade = st.text_input("Enter Grade (A-F)")
    marks = st.text_input("Enter Marks (0-100)")
    if st.button("Save"):
        ok, msg = add_student(id_, name, age, grade, marks)
        if ok: st.success(msg)
        else: st.error(msg)

elif menu == "View Students":
    st.header("All Student Records")
    students = read_students()
    if not students:
        st.info("No data found")
    else:
        for s in students:
            st.write(f"ID: {s['id_']} | Name: {s['name']} | Age: {s['age']} | Grade: {s['grade']} | Marks: {s['marks']}")

elif menu == "Search Student":
    st.header("Search Student")
    query = st.text_input("Enter ID or Name").lower()
    if st.button("Search"):
        students = read_students()
        results = [s for s in students if s['id_'] == query or query in s['name'].lower()]
        if not results:
            st.error("No record found")
        else:
            for s in results:
                st.write(f"ID: {s['id_']} | Name: {s['name']} | Age: {s['age']} | Grade: {s['grade']} | Marks: {s['marks']}")

elif menu == "Update Student":
    st.header("Update Student")
    id_ = st.text_input("Enter ID to Update")
    name = st.text_input("New Name")
    age = st.text_input("New Age")
    grade = st.text_input("New Grade (A-F)")
    marks = st.text_input("New Marks (0-100)")
    if st.button("Update"):
        ok, msg = update_student(id_, name, age, grade, marks)
        if ok: st.success(msg)
        else: st.error(msg)

elif menu == "Delete Student":
    st.header("Delete Student")
    id_ = st.text_input("Enter ID to Delete")
    if st.button("Delete"):
        ok, msg = delete_student(id_)
        if ok: st.success(msg)
        else: st.error(msg)

elif menu == "Analyze Data":
    st.header("Data Analysis")
    res = analyze_data()
    if not res:
        st.info("No data to analyze")
    else:
        st.write(f"Average Marks: {res['average']:.2f}")
        st.write(f"Top Performer: {', '.join([s['name'] for s in res['top']])} ({res['highest']})")
        st.write(f"Students Below Average: {res['below_count']}")
        st.write(f"Highest Marks: {res['highest']} | Lowest Marks: {res['lowest']}")
        st.write(f"Total Students: {res['pass_count'] + res['fail_count']}")
        st.write(f"Pass: {res['pass_count']} | Fail: {res['fail_count']}")
