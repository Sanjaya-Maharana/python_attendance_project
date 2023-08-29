from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SECRET_KEY'] = '5dd8bad83c6ac850946ed0908d7efa6e'  # Replace with your secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
logging.basicConfig(filename='app.log', level=logging.INFO)


# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    submitted_by = db.Column(db.String(80), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    submitted_by = db.Column(db.String(80), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    lecture_hours = db.Column(db.Integer, nullable=False)
    submitted_by = db.Column(db.String(80), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    department = db.relationship('Department', backref=db.backref('courses', lazy=True))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    submitted_by = db.Column(db.String(80), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    department = db.relationship('Department', backref=db.backref('students', lazy=True))

class AttendanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('attendance_logs', lazy=True))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    present = db.Column(db.Boolean, nullable=False)
    submitted_by = db.Column(db.String(80), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Create a new department
@app.route('/departments', methods=['POST'])
@login_required
def create_department():
    data = request.json
    department_name = data.get('department_name')
    submitted_by = data.get('username')

    new_department = Department(department_name=department_name, submitted_by=submitted_by)
    db.session.add(new_department)
    db.session.commit()

    return jsonify({'message': 'Department created successfully'})

# Get a list of departments
@app.route('/departments', methods=['GET'])
@login_required
def get_departments():
    departments = Department.query.all()
    department_list = [{'id': dept.id, 'department_name': dept.department_name, 'submitted_by': dept.submitted_by,
                        'updated_at': dept.updated_at} for dept in departments]

    return jsonify(department_list)

# Create a new course
@app.route('/courses', methods=['POST'])
@login_required
def create_course():
    data = request.json
    course_name = data.get('course_name')
    department_id = data.get('department_id')
    semester = data.get('semester')
    class_name = data.get('class_name')
    lecture_hours = data.get('lecture_hours')
    submitted_by = data.get("username")

    new_course = Course(course_name=course_name, department_id=department_id, semester=semester,
                        class_name=class_name, lecture_hours=lecture_hours, submitted_by=submitted_by)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({'message': 'Course created successfully'})

# Get a list of courses
@app.route('/courses', methods=['GET'])
@login_required
def get_courses():
    courses = Course.query.all()
    course_list = [{'id': course.id, 'course_name': course.course_name, 'department_id': course.department_id,
                    'semester': course.semester, 'class_name': course.class_name,
                    'lecture_hours': course.lecture_hours, 'submitted_by': course.submitted_by,
                    'updated_at': course.updated_at} for course in courses]

    return jsonify(course_list)

# Create a new student
@app.route('/students', methods=['POST'])
@login_required
def create_student():
    data = request.json
    full_name = data.get('full_name')
    department_id = data.get('department_id')
    class_name = data.get('class_name')
    submitted_by = data.get('username')

    new_student = Student(full_name=full_name, department_id=department_id, class_name=class_name,
                          submitted_by=submitted_by)
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student created successfully'})

# Get a list of students
@app.route('/students', methods=['GET'])
@login_required
def get_students():
    students = Student.query.all()
    student_list = [{'id': student.id, 'full_name': student.full_name, 'department_id': student.department_id,
                     'class_name': student.class_name, 'submitted_by': student.submitted_by,
                     'updated_at': student.updated_at} for student in students]

    return jsonify(student_list)

# Create a new attendance log
@app.route('/attendance_logs', methods=['POST'])
@login_required
def create_attendance_log():
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    present = data.get('present')
    submitted_by = data.get('username')

    new_attendance_log = AttendanceLog(student_id=student_id, course_id=course_id, present=present,
                                       submitted_by=submitted_by)
    db.session.add(new_attendance_log)
    db.session.commit()

    return jsonify({'message': 'Attendance log created successfully'})

# Get a list of attendance logs
@app.route('/attendance_logs', methods=['GET'])
@login_required
def get_attendance_logs():
    logs = AttendanceLog.query.all()
    log_list = [{'id': log.id, 'student_id': log.student_id, 'course_id': log.course_id, 'present': log.present,
                 'submitted_by': log.submitted_by, 'updated_at': log.updated_at} for log in logs]

    return jsonify(log_list)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# User Logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        with app.app_context():
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                password = 'admin123'
                hashed_password = generate_password_hash(password, method='scrypt')
                new_admin = User(username='admin', password_hash=hashed_password, user_type='admin', full_name='Admin', email='admin@example.com', submitted_by='admin')
                db.session.add(new_admin)
                db.session.commit()
                print("Admin user created. Username:", new_admin.username)
            else:
                print("User is already exist")

    app.run(debug=True,port=8000)

