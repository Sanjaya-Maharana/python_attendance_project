import requests
from datetime import datetime

login_url = 'http://127.0.0.1:8000/login'
student_url = 'http://127.0.0.1:8000/students'
headers = {'Content-Type': 'application/json'}

login_data = {
    "username": "admin",
    "password": "admin123"
}

student_data = {
    "id": 1,
    "full_name": "John Doe",
    "department_id": 1,
    "class_name": "A101",
    "username": "admin",
    "updated_at": datetime.now().isoformat()
}

login_response = requests.post(login_url, json=login_data, headers=headers)
if login_response.status_code == 200:
    print("Login successful.")

    session_cookies = login_response.cookies

    student_response = requests.post(student_url, json=student_data, headers=headers, cookies=session_cookies)

    if student_response.status_code == 201:
        print("Student created successfully.")
    else:
        print("Error creating student:", student_response.text)
else:
    print("Login failed.")
