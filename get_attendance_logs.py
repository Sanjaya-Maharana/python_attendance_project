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

    get_logs_response = requests.get(attendance_logs_url, headers=headers, cookies=session_cookies)
    if get_logs_response.status_code == 200:
        logs_list = get_logs_response.json()
        for log in logs_list:
            print("Log ID:", log['id'])
            print("Student ID:", log['student_id'])
            print("Course ID:", log['course_id'])
            print("Present:", log['present'])
            print("Submitted By:", log['submitted_by'])
            print("Updated At:", log['updated_at'])
            print("-----")
    else:
        print("Error getting attendance logs:", get_logs_response.text)
else:
    print("Login failed.")
