import requests

login_url = 'http://127.0.0.1:8000/login'
courses_url = 'http://127.0.0.1:8000/courses'
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

    new_course_data = {
        "course_name": "Introduction to Programming",
        "department_id": 1,
        "semester": "Fall 2023",
        "class_name": "CS101",
        "lecture_hours": 3,
        "username": "admin"
    }

    create_course_response = requests.post(courses_url, json=new_course_data, headers=headers, cookies=session_cookies)
    if create_course_response.status_code == 201:
        print("Course created successfully.")
    else:
        print("Error creating course:", create_course_response.text)
else:
    print("Login failed.")
