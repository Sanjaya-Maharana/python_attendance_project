import requests

login_url = 'http://127.0.0.1:8000/login'
students_url = 'http://127.0.0.1:8000/students'
headers = {'Content-Type': 'application/json'}

login_data = {
    "username": "admin",
    "password": "admin123"
}

# Perform login
login_response = requests.post(login_url, json=login_data, headers=headers)
if login_response.status_code == 200:
    print("Login successful.")

    session_cookies = login_response.cookies

    students_response = requests.get(students_url, headers=headers, cookies=session_cookies)

    if students_response.status_code == 200:
        students_list = students_response.json()
        for student in students_list:
            print("Student ID:", student['id'])
            print("Full Name:", student['full_name'])
            print("Department ID:", student['department_id'])
            print("Class Name:", student['class_name'])
            print("Submitted By:", student['submitted_by'])
            print("Updated At:", student['updated_at'])
            print("-----")
    else:
        print("Error getting students:", students_response.text)
else:
    print("Login failed.")
