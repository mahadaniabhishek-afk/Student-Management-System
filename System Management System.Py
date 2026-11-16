
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

BG = "#F5F5F5"
WHITE = "#FFFFFF"
BLACK = "#171717"
DARK = "#252525"
GREY = "#777777"
BORDER = "#DDDDDD"

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")

root = tk.Tk()
root.title("Student Management System")
root.geometry("1150x750")
root.minsize(950, 650)
root.configure(bg=BG)

students = []

def load_students():
    global students
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as file:
                data = json.load(file)
                students = data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            students = []

    for student in students:
        student.setdefault("roll", student.get("roll_number", student.get("id", "")))
        student.setdefault("name", student.get("student_name", ""))
        student.setdefault("department", student.get("course", ""))
        student.setdefault("email", student.get("email_address", ""))
        student.setdefault("phone", student.get("phone_number", ""))

def save_students():
    with open(FILE, "w") as file:
        json.dump(students, file, indent=4)

def clear_fields():
    for entry in entries.values():
        entry.delete(0, tk.END)
    selected_roll.set("")

def get_student():
    return {
        "roll": entries["Roll Number"].get().strip(),
        "name": entries["Student Name"].get().strip(),
        "department": entries["Department"].get().strip(),
        "email": entries["Email Address"].get().strip(),
        "phone": entries["Phone Number"].get().strip()
    }

def validate_student(student):
    if not all(student.values()):
        messagebox.showwarning("Missing Details", "Please fill in all fields.")
        return False

    if not student["roll"].isdigit():
        messagebox.showwarning("Invalid Roll Number", "Enter a valid numeric roll number.")
        return False

    if "@" not in student["email"] or "." not in student["email"]:
        messagebox.showwarning("Invalid Email", "Enter a valid email address.")
        return False

    if not student["phone"].isdigit() or len(student["phone"]) != 10:
        messagebox.showwarning("Invalid Phone", "Enter a 10-digit phone number.")
        return False

    return True

def refresh_table(data=None):
    table.delete(*table.get_children())
    records = students if data is None else data

    for student in records:
        table.insert("", tk.END, values=(
            student.get("roll", ""),
            student.get("name", ""),
            student.get("department", ""),
            student.get("email", ""),
            student.get("phone", "")
        ))

    total_label.config(text=f"{len(students):02d} STUDENTS")

def add_student():
    student = get_student()

    if not validate_student(student):
        return

    if any(str(s.get("roll", "")) == student["roll"] for s in students):
        messagebox.showerror("Duplicate", "This roll number already exists.")
        return

    students.append(student)
    save_students()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student added successfully.")

def select_student(event=None):
    selected = table.selection()

    if not selected:
        return

    values = table.item(selected[0], "values")
    clear_fields()

    labels = [
        "Roll Number",
        "Student Name",
        "Department",
        "Email Address",
        "Phone Number"
    ]

    for label, value in zip(labels, values):
        entries[label].insert(0, value)

    selected_roll.set(str(values[0]))

def update_student():
    roll = selected_roll.get()

    if not roll:
        messagebox.showwarning("Select Student", "Select a student from the table first.")
        return

    student = get_student()

    if not validate_student(student):
        return

    if student["roll"] != roll and any(
        str(s.get("roll", "")) == student["roll"] for s in students
    ):
        messagebox.showerror("Duplicate", "This roll number already exists.")
        return

    for index, old in enumerate(students):
        if str(old.get("roll", "")) == roll:
            students[index] = student
            break

    save_students()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student updated successfully.")

def delete_student():
    roll = selected_roll.get()

    if not roll:
        messagebox.showwarning("Select Student", "Select a student from the table first.")
        return

    if not messagebox.askyesno("Confirm Delete", "Delete this student record?"):
        return

    students[:] = [
        s for s in students
        if str(s.get("roll", "")) != roll
    ]

    save_students()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Deleted", "Student record deleted.")

def search_student():
    keyword = search_entry.get().strip().lower()

    if not keyword:
        refresh_table()
        return

    results = [
        s for s in students
        if keyword in str(s.get("name", "")).lower()
        or keyword in str(s.get("roll", "")).lower()
    ]

    refresh_table(results)

def show_all():
    search_entry.delete(0, tk.END)
    refresh_table()

def make_button(parent, text, command, background=WHITE, foreground=BLACK):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=background,
        fg=foreground,
        activebackground="#E8E8E8",
        activeforeground=BLACK,
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=11
    )

selected_roll = tk.StringVar()

sidebar = tk.Frame(root, bg=BLACK, width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="STUDENT\nMANAGEMENT",
    bg=BLACK,
    fg=WHITE,
    font=("Arial", 19, "bold"),
    justify="left"
).pack(anchor="w", padx=25, pady=(40, 8))

tk.Label(
    sidebar,
    text="ADMIN DASHBOARD",
    bg=BLACK,
    fg="#AAAAAA",
    font=("Arial", 9)
).pack(anchor="w", padx=25, pady=(0, 50))

tk.Label(
    sidebar,
    text="MAIN MENU",
    bg=BLACK,
    fg="#888888",
    font=("Arial", 9, "bold")
).pack(anchor="w", padx=25, pady=(0, 15))

make_button(sidebar, "⌂   Dashboard", show_all, DARK, WHITE).pack(fill="x", padx=15, pady=5)
make_button(sidebar, "+   Add Student", clear_fields, BLACK, WHITE).pack(fill="x", padx=15, pady=5)
make_button(sidebar, "▤   View Students", show_all, BLACK, WHITE).pack(fill="x", padx=15, pady=5)

tk.Frame(sidebar, bg="#444444", height=1).pack(fill="x", padx=20, pady=30)

tk.Label(
    sidebar,
    text="STUDENT RECORD SYSTEM\nVersion 1.0",
    bg=BLACK,
    fg="#888888",
    font=("Arial", 9),
    justify="left"
).pack(side="bottom", anchor="w", padx=25, pady=25)

main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

header = tk.Frame(main, bg=WHITE, height=75)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="Dashboard",
    bg=WHITE,
    fg=BLACK,
    font=("Arial", 20, "bold")
).pack(side="left", padx=30)

tk.Label(
    header,
    text="STUDENT RECORDS",
    bg=WHITE,
    fg=GREY,
    font=("Arial", 9, "bold")
).pack(side="right", padx=30)

content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True, padx=30, pady=25)

tk.Label(
    content,
    text="Student Overview",
    bg=BG,
    fg=BLACK,
    font=("Arial", 21, "bold")
).pack(anchor="w")

tk.Label(
    content,
    text="Manage student information and academic records.",
    bg=BG,
    fg=GREY,
    font=("Arial", 10)
).pack(anchor="w", pady=(5, 20))

summary = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
summary.pack(fill="x", pady=(0, 20))

tk.Label(
    summary,
    text="TOTAL REGISTERED STUDENTS",
    bg=WHITE,
    fg=GREY,
    font=("Arial", 9, "bold")
).pack(anchor="w", padx=20, pady=(15, 5))

total_label = tk.Label(
    summary,
    text="00 STUDENTS",
    bg=WHITE,
    fg=BLACK,
    font=("Arial", 23, "bold")
)
total_label.pack(anchor="w", padx=20, pady=(0, 15))

form_card = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
form_card.pack(fill="x", pady=(0, 20))

tk.Label(
    form_card,
    text="Student Information",
    bg=WHITE,
    fg=BLACK,
    font=("Arial", 14, "bold")
).pack(anchor="w", padx=20, pady=(15, 12))

form_grid = tk.Frame(form_card, bg=WHITE)
form_grid.pack(fill="x", padx=20, pady=(0, 15))

entries = {}
fields = [
    "Roll Number",
    "Student Name",
    "Department",
    "Email Address",
    "Phone Number"
]

for i, field in enumerate(fields):
    r, c = divmod(i, 3)

    cell = tk.Frame(form_grid, bg=WHITE)
    cell.grid(row=r, column=c, sticky="ew", padx=(0, 15), pady=7)

    tk.Label(
        cell,
        text=field,
        bg=WHITE,
        fg=GREY,
        font=("Arial", 9, "bold")
    ).pack(anchor="w", pady=(0, 5))

    entry = tk.Entry(
        cell,
        font=("Arial", 10),
        bg=WHITE,
        fg=BLACK,
        relief="solid",
        bd=1,
        highlightthickness=0
    )
    entry.pack(fill="x", ipady=8)
    entries[field] = entry

for c in range(3):
    form_grid.columnconfigure(c, weight=1)

actions = tk.Frame(form_card, bg=WHITE)
actions.pack(fill="x", padx=20, pady=(0, 15))

make_button(actions, "ADD STUDENT", add_student, BLACK, WHITE).pack(side="left", padx=(0, 8))
make_button(actions, "UPDATE", update_student).pack(side="left", padx=8)
make_button(actions, "DELETE", delete_student).pack(side="left", padx=8)
make_button(actions, "CLEAR", clear_fields).pack(side="right")

table_card = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_card.pack(fill="both", expand=True)

table_header = tk.Frame(table_card, bg=WHITE)
table_header.pack(fill="x", padx=20, pady=15)

tk.Label(
    table_header,
    text="Registered Students",
    bg=WHITE,
    fg=BLACK,
    font=("Arial", 14, "bold")
).pack(side="left")

search_entry = tk.Entry(
    table_header,
    font=("Arial", 10),
    relief="solid",
    bd=1,
    width=22
)
search_entry.pack(side="right", ipady=7, padx=(8, 0))

make_button(
    table_header,
    "SEARCH",
    search_student,
    BLACK,
    WHITE
).pack(side="right")

table_frame = tk.Frame(table_card, bg=WHITE)
table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=BLACK,
    fieldbackground=WHITE,
    rowheight=35,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#EAEAEA",
    foreground=BLACK,
    font=("Arial", 9, "bold"),
    relief="flat"
)

style.map(
    "Treeview",
    background=[("selected", "#D9D9D9")],
    foreground=[("selected", BLACK)]
)

columns = ("roll", "name", "department", "email", "phone")
table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

headings = {
    "roll": "ROLL NO.",
    "name": "STUDENT NAME",
    "department": "DEPARTMENT",
    "email": "EMAIL ADDRESS",
    "phone": "PHONE NUMBER"
}

widths = {
    "roll": 80,
    "name": 150,
    "department": 150,
    "email": 190,
    "phone": 120
}

for col in columns:
    table.heading(col, text=headings[col])
    table.column(
        col,
        width=widths[col],
        minwidth=70,
        anchor="center"
    )

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)
table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

table.bind("<<TreeviewSelect>>", select_student)

load_students()
refresh_table()

root.mainloop()
