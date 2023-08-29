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

    # Get a list of courses
    get_courses_response = requests.get(courses_url, headers=headers, cookies=session_cookies)
    if get_courses_response.status_code == 200:
        courses_list = get_courses_response.json()
        for course in courses_list:
            print("Course ID:", course['id'])
            print("Course Name:", course['course_name'])
            print("Department ID:", course['department_id'])
            print("Semester:", course['semester'])
            print("Class Name:", course['class_name'])
            print("Lecture Hours:", course['lecture_hours'])
            print("Submitted By:", course['submitted_by'])
            print("Updated At:", course['updated_at'])
            print("-----")
    else:
        print("Error getting courses:", get_courses_response.text)
else:
    print("Login failed.")
