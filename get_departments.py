import requests

login_url = 'http://127.0.0.1:8000/login'
departments_url = 'http://127.0.0.1:8000/departments'
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

    departments_response = requests.get(departments_url, headers=headers, cookies=session_cookies)

    if departments_response.status_code == 200:
        departments_list = departments_response.json()
        for department in departments_list:
            print("Department ID:", department['id'])
            print("Department Name:", department['department_name'])
            print("Submitted By:", department['submitted_by'])
            print("-----")
    else:
        print("Error getting departments:", departments_response.text)
else:
    print("Login failed.")
