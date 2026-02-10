import mysql.connector
from mysql.connector import Error
import csv
import os

# ------------------- Connect to MySQL -------------------
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
        cursor.execute("USE student_db")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                grade VARCHAR(10) NOT NULL
            )
        """)
        conn.commit()
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ------------------- Add Student -------------------
def add_student(conn, name, age, grade):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
        conn.commit()
        print(f"Student '{name}' added successfully.")
        save_to_file(name, age, grade)
    except Error as e:
        print(f"Error adding student: {e}")

# ------------------- View Students -------------------
def view_students(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        if rows:
            print("\nAll Students:")
            for row in rows:
                print(row)
        else:
            print("No students found.")
    except Error as e:
        print(f"Error fetching students: {e}")

# ------------------- Update Student -------------------
def update_student(conn, student_id, name=None, age=None, grade=None):
    try:
        cursor = conn.cursor()
        if name:
            cursor.execute("UPDATE students SET name=%s WHERE id=%s", (name, student_id))
        if age:
            cursor.execute("UPDATE students SET age=%s WHERE id=%s", (age, student_id))
        if grade:
            cursor.execute("UPDATE students SET grade=%s WHERE id=%s", (grade, student_id))
        conn.commit()
        print(f"Student ID {student_id} updated successfully.")
    except Error as e:
        print(f"Error updating student: {e}")

# ------------------- Delete Student -------------------
def delete_student(conn, student_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        conn.commit()
        print(f"Student ID {student_id} deleted successfully.")
    except Error as e:
        print(f"Error deleting student: {e}")

# ------------------- Backup to CSV File -------------------
def save_to_file(name, age, grade):
    try:
        file_exists = os.path.isfile("students_backup.csv")
        with open("students_backup.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Name", "Age", "Grade"])  # header
            writer.writerow([name, age, grade])
    except Exception as e:
        print(f"Error saving to file: {e}")

# ------------------- Interactive Menu -------------------
def menu():
    conn = create_connection()
    if not conn:
        return

    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter choice (1-5): ")

        if choice == "1":
            try:
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                grade = input("Enter grade: ")
                add_student(conn, name, age, grade)
            except ValueError:
                print("Invalid input. Age must be a number.")
        elif choice == "2":
            view_students(conn)
        elif choice == "3":
            try:
                student_id = int(input("Enter student ID to update: "))
                name = input("Enter new name (leave blank to skip): ")
                age_input = input("Enter new age (leave blank to skip): ")
                age = int(age_input) if age_input else None
                grade = input("Enter new grade (leave blank to skip): ")
                update_student(conn, student_id, name=name if name else None, age=age, grade=grade if grade else None)
            except ValueError:
                print("Invalid input. ID and Age must be numbers.")
        elif choice == "4":
            try:
                student_id = int(input("Enter student ID to delete: "))
                delete_student(conn, student_id)
            except ValueError:
                print("Invalid input. ID must be a number.")
        elif choice == "5":
            conn.close()
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Enter 1-5.")

# ------------------- Run Program -------------------
if __name__ == "__main__":
    menu()
