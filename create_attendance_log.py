import requests

login_url = 'http://127.0.0.1:8000/login'
attendance_logs_url = 'http://127.0.0.1:8000/attendance_logs'
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
    new_log_data = {
        "student_id": 1,
        "course_id": 1,
        "present": True,
        "username": "admin"
    }

    create_log_response = requests.post(attendance_logs_url, json=new_log_data, headers=headers, cookies=session_cookies)
    if create_log_response.status_code == 201:
        print("Attendance log created successfully.")
    else:
        print("Error creating attendance log:", create_log_response.text)
else:
    print("Login failed.")
