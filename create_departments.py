import requests

login_url = 'http://127.0.0.1:8000/login'
department_url = 'http://127.0.0.1:8000/departments'
headers = {'Content-Type': 'application/json'}

login_data = {
    "username": "admin",
    "password": "admin123"
}

department_data = {
    "department_name": "Computer Science",
    "username": "admin",
}

# Perform login
login_response = requests.post(login_url, json=login_data, headers=headers)
if login_response.status_code == 200:
    print("Login successful.")

    session_cookies = login_response.cookies

    department_response = requests.post(department_url, json=department_data, headers=headers, cookies=session_cookies)

    if department_response.status_code == 201:
        print("Department created successfully.")
    else:
        print("Error creating department:", department_response.text)
else:
    print("Login failed.")
