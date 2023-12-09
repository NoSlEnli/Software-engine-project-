import mysql.connector as mysql
import os
import re
import datetime

db = mysql.connect(host="localhost",user="root",password="",database="college")
command_handler = db.cursor(buffered=True)

def register_user(privilege):
    username = input(f"{privilege.capitalize()} username: ")
    password = input(f"{privilege.capitalize()} password: ")
    command_handler.execute(f"SELECT user_id FROM users WHERE privilage = %s ORDER BY user_id DESC LIMIT 1", (privilege,))
    last_user_id = command_handler.fetchone()
    if last_user_id:
        last_id_number = int(last_user_id[0][1:])
        new_id_number = last_id_number + 1
    else:
        new_id_number = 1
    user_id = f"{'t' if privilege == 'teacher' else 's'}{str(new_id_number).zfill(8)}"
    command_handler.execute("INSERT INTO users (user_id, username, password, privilage) VALUES (%s, %s, %s, %s)", (user_id, username, password, privilege))
    db.commit()
    print(f"{privilege.capitalize()} registered with ID: {user_id}")

def validate_telephone():
    while True:
        telephone = input("Telephone (8 digits): ")
        if len(telephone) == 8 and telephone.isdigit():
            return telephone
        else:
            print("Invalid telephone number. Please enter 8 digits.")

def validate_sex():
    while True:
        sex = input("Sex (M/F): ").upper()
        if sex in ['M', 'F']:
            return sex
        else:
            print("Invalid input. Please enter 'M' or 'F'.")

def validate_hkid():
    hkid_pattern = re.compile(r'^[A-Z]{1,2}\d{6,7}$')
    while True:
        hkid = input("HKID (e.g., Y1234567, XA123456): ").upper()
        if hkid_pattern.match(hkid):
            return hkid
        else:
            print("Invalid HKID format. Please enter as shown in examples.")

def validate_date():
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    while True:
        date_input = input("Date (YYYY-MM-DD): ")
        if date_pattern.match(date_input):
            try:
                year, month, day = map(int, date_input.split('-'))
                datetime.date(year, month, day)
                return date_input
            except ValueError:
                print("Invalid date. Please enter a valid date in YYYY-MM-DD format.")
        else:
            print("Invalid format. Please enter date in YYYY-MM-DD format.")

def validate_status(student_id, student_name):
    while True:
        status = input(f"Status for {student_id} {student_name} (P/A/L): ").upper()
        if status in ['P', 'A', 'L']:
            return status
        else:
            print("Invalid status. Please enter 'P', 'A', or 'L'.")

def get_valid_grade(course_name):
    valid_grades = ['A', 'B', 'C', 'D', 'F']
    while True:
        grade = input(f"Enter grade for {course_name} (A, B, C, D, F): ").upper()
        if grade in valid_grades:
            return grade
        else:
            print("Invalid grade. Please enter A, B, C, D, or F.")
                        
def student_session(user_id):
    while True:
        print("\nStudent's Menu\n")
        print("1. View Register")
        print("2. View Personal Information")
        print("3. Edit Personal Information")
        print("4. View Grade")
        print("5. Download Register")
        print("6. Download Personal Information")
        print("7. Download Transcript")
        print("8. Logout")

        user_option = input("Option : ")
        if user_option == "1":
            print("Displaying register")
            query_vals = (user_id,)
            command_handler.execute("SELECT date, status FROM attendance WHERE user_id = %s ORDER BY date", query_vals)
            records = command_handler.fetchall()
            
            for record in records:
                formatted_date = record[0].strftime('%Y/%m/%d')
                print(f"{formatted_date}, '{record[1]}'")

        elif user_option == "2":
            print("Displaying personal information")
            query_vals = (user_id,)
            command_handler.execute("SELECT username, address, telephone, sex, hkid FROM address WHERE user_id = %s", query_vals)
            records = command_handler.fetchall()
            for record in records:
                print(record)

        elif user_option == "3":
            print("Editing personal information")

            command_handler.execute("SELECT address, telephone, sex, hkid FROM address WHERE user_id = %s", (user_id,))
            current_info = command_handler.fetchone()

            if current_info:
                print(f"Current Information: Address: {current_info[0]}, Telephone: {current_info[1]}, Sex: {current_info[2]}, HKID: {current_info[3]}")
                new_address = input("New Address (press enter to keep current): ") or current_info[0]

                new_telephone_input = input("New Telephone (press enter to keep current): ")
                new_telephone = validate_telephone() if new_telephone_input else current_info[1]

                new_sex_input = input("New Sex (M/F, press enter to keep current): ").upper()
                new_sex = validate_sex() if new_sex_input else current_info[2]

                new_hkid_input = input("New HKID (press enter to keep current): ")
                new_hkid = validate_hkid() if new_hkid_input else current_info[3]
            else:
                print("No existing personal information found. Please enter new information.")
                new_address = input("New Address: ")
                new_telephone = validate_telephone()
                new_sex = validate_sex()
                new_hkid = validate_hkid()

            command_handler.execute("SELECT username FROM users WHERE user_id = %s", (user_id,))
            current_username = command_handler.fetchone()[0] if command_handler.rowcount > 0 else ''

            if current_info:
                query_vals = (new_address, new_telephone, new_sex, new_hkid, user_id)
                command_handler.execute("UPDATE address SET address = %s, telephone = %s, sex = %s, hkid = %s WHERE user_id = %s", query_vals)
            else:
                query_vals = (user_id, current_username, new_address, new_telephone, new_sex, new_hkid)
                command_handler.execute("INSERT INTO address (user_id, username, address, telephone, sex, hkid) VALUES (%s, %s, %s, %s, %s, %s)", query_vals)

            db.commit()
            print("Information Updated.")

        elif user_option == "4":
            print("Displaying grade")
            query_vals = (user_id,)
            command_handler.execute("SELECT java, db, ss, softwareengine FROM mark WHERE user_id = %s", query_vals)
            print("Java Application Development || Database Management || Software Engineering || Server-side Technologies And Cloud Computing ")
            records = command_handler.fetchall()
            for record in records:
                print(record)

        elif user_option == "5":
            print("Downloading Register")
            query_vals = (user_id,)
            command_handler.execute("SELECT date, status FROM attendance WHERE user_id = %s", query_vals)
            records = command_handler.fetchall()
            report_path = os.path.join(os.path.dirname(__file__), f'register_report_{user_id}.txt')
            with open(report_path, "w") as f:
                for record in records:
                    f.write(str(record) + "\n")
            print("Register has been saved to " + report_path)

        elif user_option == "6":
            print("Downloading personal information")
            query_vals = (user_id,)
            command_handler.execute("SELECT address, telephone, sex, hkid FROM address WHERE user_id = %s", query_vals)
            records = command_handler.fetchall()
            report_path = os.path.join(os.path.dirname(__file__), f'personal_info_report_{user_id}.txt')
            with open(report_path, "w") as f:
                for record in records:
                    f.write(str(record) + "\n")
            print("Personal information has been saved to " + report_path)

        elif user_option == "7":
            print("Downloading transcript")
            query_vals = (user_id,)
            command_handler.execute("SELECT java, db, ss, softwareengine FROM mark WHERE user_id = %s", query_vals)
            records = command_handler.fetchall()
            report_path = os.path.join(os.path.dirname(__file__), f'transcript_report_{user_id}.txt')
            with open(report_path, "w") as f:
                for record in records:
                    f.write(str(record) + "\n")
            print("Transcript has been saved to " + report_path)

        elif user_option == "8":
            break
        else:
            print("No valid option was selected.")

def teacher_session(teacher_id):
    while True:
        print("\nTeacher's Menu\n")
        print("1. Mark Student Register")
        print("2. Grade Student Mark")
        print("3. View Register")
        print("4. Logout")

        user_option = input("Option : ")
        if user_option == "1":
            print("\nMark Student Register")
            date = validate_date()
            command_handler.execute("SELECT user_id, username FROM users WHERE privilage = 'student'")
            student_records = command_handler.fetchall()
            
            for student_id, student_name in student_records:
                status = validate_status(student_id, student_name)
                query_vals = (student_id, student_name, date, status)
                command_handler.execute("INSERT INTO attendance (user_id, username, date, status) VALUES (%s, %s, %s, %s)", query_vals)
                db.commit()
                print(f"{student_id} {student_name} marked as {status}")

        elif user_option == "2":
            while True:
                print("\nGrading Student Mark")
                student_name = input("Student name (or type 'exit' to go back): ")
                if student_name.lower() == 'exit':
                    break

                command_handler.execute("SELECT user_id, username FROM users WHERE username = %s AND privilage = 'student'", (student_name,))
                results = command_handler.fetchall()

                if not results:
                    print("Student not found. Please try again.")
                    continue

                if len(results) > 1:
                    print("Multiple students found with this username. Please select by user ID:")
                    for student_id, name in results:
                        print(f"User ID: {student_id}, Name: {name}")
                    student_id = input("Enter Student User ID: ")
                    if not any(student_id == row[0] for row in results):
                        print("Invalid User ID entered. Please try again.")
                        continue
                    student_username = [row[1] for row in results if row[0] == student_id][0]
                else:
                    student_id = results[0][0]
                    student_username = results[0][1]

                command_handler.execute("SELECT java, db, ss, softwareengine FROM mark WHERE user_id = %s", (student_id,))
                grades = command_handler.fetchone()

                if grades:
                    print(f"Current Grades: Java: {grades[0]}, Database: {grades[1]}, Server-Side: {grades[2]}, Software Engineering: {grades[3]}")
                    modify = input("Detected that the student's grades have been entered. Do you want to modify them? (yes/no): ").lower()
                    if modify != 'yes':
                        break

                java = get_valid_grade("Java Application Development")
                db_mark = get_valid_grade("Database Management")
                ss = get_valid_grade("Server-Side Technologies")
                software_engine = get_valid_grade("Software Engineering")

                if grades:
                    command_handler.execute("UPDATE mark SET java = %s, db = %s, ss = %s, softwareengine = %s, username = %s WHERE user_id = %s", (java, db_mark, ss, software_engine, student_username, student_id))
                else:
                    command_handler.execute("INSERT INTO mark (user_id, username, java, db, ss, softwareengine) VALUES (%s, %s, %s, %s, %s, %s)", (student_id, student_username, java, db_mark, ss, software_engine))
                db.commit()
                print(f"{student_name}'s grades have been updated.")
                break

        elif user_option == "3":
            print("\nViewing All Student Registers")
            command_handler.execute("SELECT users.user_id, users.username, attendance.date, attendance.status FROM attendance INNER JOIN users ON attendance.user_id = users.user_id WHERE users.privilage = 'student' ORDER BY users.user_id, attendance.date")
            records = command_handler.fetchall()

            print("Displaying All Registers")
            last_user_id = None
            for record in records:
                user_id, username, date, status = record
                formatted_date = date.strftime('%Y/%m/%d')

                if last_user_id != user_id:
                    print()
                    last_user_id = user_id

                print(f"('{user_id}', '{username}', '{formatted_date}', '{status}')")


        elif user_option == "4":
            break
        else:
            print("No valid option was selected.")

def admin_session():
    while True:
        print("\nAdmin Menu\n")
        print("1. Register New Student")
        print("2. Register Student Personal Information")
        print("3. View/Edit Student Personal Information")
        print("4. Register New Teacher")
        print("5. Change User Password")
        print("6. List All Students")
        print("7. List All Teachers")
        print("8. Delete Existing Student")
        print("9. Delete Existing Teacher")
        print("10. Logout")
        

        user_option = input("Option : ")
        if user_option == "1":
            register_user("student")

        elif user_option == "2":
            while True:
                print("\nRegister Student Personal Information")
                username = input("Student Username (or type 'exit' to go back): ")
                if username.lower() == 'exit':
                    break

                command_handler.execute("SELECT user_id, username FROM users WHERE username = %s AND privilage = 'student'", (username,))
                results = command_handler.fetchall()

                if not results:
                    print("Student not found. Please try again.")
                    continue

                if len(results) > 1:
                    print("Multiple students found with this username. Please select by user ID:")
                    for user_id, name in results:
                        print(f"User ID: {user_id}, Name: {name}")
                    student_id = input("Enter Student User ID: ")
                    if not any(student_id == row[0] for row in results):
                        print("Invalid User ID entered. Please try again.")
                        continue
                else:
                    student_id = results[0][0]

                command_handler.execute("SELECT address, telephone, sex, hkid FROM address WHERE user_id = %s", (student_id,))
                personal_info = command_handler.fetchone()
                if personal_info:
                    print(f"Current Personal Information for {username}: Address: {personal_info[0]}, Telephone: {personal_info[1]}, Sex: {personal_info[2]}, HKID: {personal_info[3]}")
                    edit = input("Student personal information already exists. Do you want to edit it? (yes/no): ").lower()
                    if edit == 'yes':
                        new_username = input("Enter new username for the student (leave blank to keep the same): ")
                        new_address = input("New Address: ")
                        new_telephone = validate_telephone()
                        new_sex = validate_sex()
                        new_hkid = validate_hkid()
                        update_vals = (new_address, new_telephone, new_sex, new_hkid, student_id)
                        if new_username and new_username != username:
                            command_handler.execute("UPDATE users SET username = %s WHERE user_id = %s", (new_username, student_id))
                            command_handler.execute("UPDATE address SET username = %s WHERE user_id = %s", (new_username, student_id))
                            command_handler.execute("UPDATE attendance SET username = %s WHERE user_id = %s", (new_username, student_id))
                            command_handler.execute("UPDATE mark SET username = %s WHERE user_id = %s", (new_username, student_id))                            
                            db.commit()
                            username = new_username
                        command_handler.execute("UPDATE address SET address = %s, telephone = %s, sex = %s, hkid = %s WHERE user_id = %s", update_vals)
                        db.commit()
                        print(f"Personal information for {username} with ID {student_id} has been updated.")
                else:
                    address = input("Student Address: ")
                    telephone = validate_telephone()
                    sex = validate_sex()
                    hkid = validate_hkid()
                    command_handler.execute("INSERT INTO address (user_id, address, telephone, sex, hkid) VALUES (%s, %s, %s, %s, %s)", (student_id, address, telephone, sex, hkid))
                    db.commit()
                    print(f"{username}'s personal information has been registered.")

        elif user_option == "3":
            while True:
                print("View/Edit Student Personal Information")
                username = input("Enter Student Username (or type 'exit' to go back): ")
                if username.lower() == 'exit':
                    break

                command_handler.execute("SELECT user_id, username FROM users WHERE username = %s AND privilage = 'student'", (username,))
                results = command_handler.fetchall()

                if not results:
                    print("Student not found. Please try again.")
                    continue

                if len(results) > 1:
                    print("Multiple students found with this username. Please select by user ID:")
                    for user_id, name in results:
                        print(f"User ID: {user_id}, Name: {name}")
                    student_id = input("Enter Student User ID: ")
                    if not any(student_id == row[0] for row in results):
                        print("Invalid User ID entered. Please try again.")
                        continue
                else:
                    student_id = results[0][0]

                command_handler.execute("SELECT address, telephone, sex, hkid FROM address WHERE user_id = %s", (student_id,))
                personal_info = command_handler.fetchone()
                if personal_info:
                    print(f"Current Personal Information: Address: {personal_info[0]}, Telephone: {personal_info[1]}, Sex: {personal_info[2]}, HKID: {personal_info[3]}")
                    update = input("Do you want to update this information? (yes/no): ").lower()
                    if update == "yes":
                        new_username = input("Enter new username for the student (leave blank to keep the same): ")
                        new_address = input("New Address: ")
                        new_telephone = validate_telephone()
                        new_sex = validate_sex()
                        new_hkid = validate_hkid()
                        update_vals = (new_address, new_telephone, new_sex, new_hkid, student_id)
                        if new_username and new_username != username:
                            command_handler.execute("UPDATE users SET username = %s WHERE user_id = %s", (new_username, student_id))
                            command_handler.execute("UPDATE address SET username = %s WHERE user_id = %s", (new_username, student_id))
                            command_handler.execute("UPDATE attendance SET username = %s WHERE user_id = %s", (new_username, student_id))
                            command_handler.execute("UPDATE mark SET username = %s WHERE user_id = %s", (new_username, student_id))
                            db.commit()
                            username = new_username
                        command_handler.execute("UPDATE address SET address = %s, telephone = %s, sex = %s, hkid = %s WHERE user_id = %s", update_vals)
                        db.commit()
                        print(f"Personal information for {username} with ID {student_id} has been updated.")
                else:
                    print("No personal information found for this student.")

                break

        elif user_option == "4":
            register_user("teacher")

        elif user_option == "5":
            print("\nChanging user password")
            user_id = input("Enter the student/teacher ID to change password: ")

            command_handler.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            if command_handler.rowcount == 0:
                print("User ID not found.")
                continue

            new_password = input("Enter the new password: ")
            
            command_handler.execute("UPDATE users SET password = %s WHERE user_id = %s", (new_password, user_id))
            db.commit()
            print(f"Password for user ID {user_id} has been updated.")

        elif user_option == "6":
            print("\nList of All Students")
            command_handler.execute("SELECT user_id, username FROM users WHERE privilage = 'student'")
            students = command_handler.fetchall()
            for student in students:
                print(f"Student ID: {student[0]}, Userame: {student[1]}")

        elif user_option == "7":
            print("\nList of All Teachers")
            command_handler.execute("SELECT user_id, username FROM users WHERE privilage = 'teacher'")
            teachers = command_handler.fetchall()
            for teacher in teachers:
                print(f"Teacher ID: {teacher[0]}, Userame: {teacher[1]}")

        elif user_option == "8":
            while True:
                print("\nDelete Existing Student Account")
                username = input("Student Username (or type 'exit' to go back): ")
                if username.lower() == 'exit':
                    break

                command_handler.execute("SELECT user_id, username FROM users WHERE username = %s AND privilage = 'student'", (username,))
                results = command_handler.fetchall()

                if not results:
                    print("Student not found. Please try again.")
                    continue

                if len(results) > 1:
                    print("Multiple students found with this username. Please select by user ID:")
                    for user_id, name in results:
                        print(f"User ID: {user_id}, Name: {name}")
                    student_id = input("Enter Student User ID: ")
                    if not any(student_id == row[0] for row in results):
                        print("Invalid User ID entered. Please try again.")
                        continue
                else:
                    student_id = results[0][0]

                command_handler.execute("DELETE FROM address WHERE user_id = %s", (student_id,))
                command_handler.execute("DELETE FROM attendance WHERE user_id = %s", (student_id,))
                command_handler.execute("DELETE FROM mark WHERE user_id = %s", (student_id,))
                db.commit()

                command_handler.execute("DELETE FROM users WHERE user_id = %s", (student_id,))
                db.commit()
                print(f"Student account with ID {student_id} has been deleted.")
                break

        elif user_option == "9":
            while True:
                print("\nDelete Existing Teacher Account")
                username = input("Teacher Username (or type 'exit' to go back): ")
                if username.lower() == 'exit':
                    break

                command_handler.execute("SELECT user_id, username FROM users WHERE username = %s AND privilage = 'teacher'", (username,))
                results = command_handler.fetchall()

                if not results:
                    print("Teacher not found. Please try again.")
                    continue

                if len(results) > 1:
                    print("Multiple teachers found with this username. Please select by user ID:")
                    for user_id, name in results:
                        print(f"User ID: {user_id}, Name: {name}")
                    teacher_id = input("Enter Teacher User ID: ")
                    if not any(teacher_id == row[0] for row in results):
                        print("Invalid User ID entered. Please try again.")
                        continue
                else:
                    teacher_id = results[0][0]

                command_handler.execute("DELETE FROM users WHERE user_id = %s", (teacher_id,))
                db.commit()
                print(f"Teacher account with ID {teacher_id} has been deleted.")
                break

        elif user_option == "10":
            break

        else:
            print("No valid option selected.")

def auth_student():
    print("\nLogging in as Student\n")
    user_id = input("User ID: ")
    password = input("Password: ")
    query_vals = (user_id, password, "student")
    command_handler.execute("SELECT * FROM users WHERE user_id = %s AND password = %s AND privilage = %s", query_vals)
    if command_handler.rowcount > 0:
        student_session(user_id)
    else:
        print("Login details are not recognized.")

def auth_teacher():
    print("\nLogging in as Teacher\n")
    user_id = input("User ID: ")
    password = input("Password: ")
    query_vals = (user_id, password, "teacher")
    command_handler.execute("SELECT * FROM users WHERE user_id = %s AND password = %s AND privilage = %s", query_vals)
    if command_handler.rowcount > 0:
        teacher_session(user_id)
    else:
        print("Login details are not recognized.")

def auth_admin():
    print("\nLogging in as Admin\n")
    username = input("Username : ")
    password = input("Password : ")
    if username == "admin":
        if password == "password":
            admin_session()
        else:
            print("The password is incorrect.")
    else:
        print("Login details are not recognised.")  

def main():
    while 1:
        print("\nThe School of Science and Technology\n")
        print("Welcome to the School Management system")
        print("")
        print("1. Login as student")
        print("2. Login as teacher")
        print("3. Login as admin")
        print("4. Quit")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        elif user_option == "4":
            print("Exiting the system.")
            break
        else:
            print("No valid option was selected.")

main()