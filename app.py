from flask_socketio import SocketIO
from flask import g, Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
from flask import Response,jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt
import  sys, numpy as np, json, os, base64, joblib
from io import BytesIO
import os, io, base64, logging
from time import sleep
import pandas as pd
from werkzeug.utils import secure_filename 
import subprocess
import random
from flask_mail import Mail, Message
import pandas as pd
app = Flask(__name__, static_folder='static')
from geopy.distance import geodesic

AISSMS_COORDINATES = (18.505437627232865, 73.95293901495018)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

socketio = SocketIO(app)

# Use SQLite database file named 'users.db' located in the project directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

# Configuration for Gmail SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tester.720.lol@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'eggi fpqq yrbb hnqt'   # Replace with your password or app-specific password

mail = Mail(app)


class Authenticate(db.Model, UserMixin):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.username} - {self.password}"
    def get_id(self):
        return str(self.sno)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    batch = db.Column(db.Integer, unique=False, nullable = False)
    def __repr__(self):
        return f"{self.roll_number} - {self.name}"

# class AttendanceRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     roll_no = db.Column(db.String(20), unique=True, nullable=False)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(20), unique=True, nullable=False)
#     subject_name = db.Column(db.String(200),nullable=False)
#     batch = db.Column(db.String(20))
#     slot_type = db.Column(db.String(200),nullable=False)
#     date = db.Column(db.Date,nullable=False)
#     present = db.Column(db.String(1),default='n') # n means absent

#     def __repr__(self):
#         return f"{self.roll_number} - {self.name}"

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date,nullable=False)
    batch = db.Column(db.String(20),nullable=False)
    slot = db.Column(db.String(200),nullable=False)
    roll_no = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    present = db.Column(db.String(1),default='n') # n means absent


class TeacherMap(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    teacherName = db.Column(db.String(200), nullable=False, unique=True)
    subject = db.Column(db.String(200), nullable=False)


class TimeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    slot1 = db.Column(db.String(200))
    slot2 = db.Column(db.String(200))
    slot3 = db.Column(db.String(200))
    slot4 = db.Column(db.String(200))
    slot5 = db.Column(db.String(200))
    slot6 = db.Column(db.String(200))
    slot7 = db.Column(db.String(200))
    slot8 = db.Column(db.String(200))
    def __repr__(self):
        return f"{self.day}"

class markedAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date,nullable=False)
    batch = db.Column(db.String(20),nullable=False)
    slot = db.Column(db.String(200),nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Authenticate.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']

        user = Authenticate.query.filter_by(username=uname).first()
        if user and (user.password == pwd):
            login_user(user)
            if current_user.is_authenticated:
                flash('Login Successful!','info')

            session['role'] = user.role
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html") 



@app.route("/showAdmin")
@login_required
def showAdmin():
    return render_template("admin.html") 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

@app.route('/addstudent')
def to_addStudent():
    return render_template('addStudent.html')

@app.route('/uploadStudentData')
def to_uploadStudentData():
    return render_template('uploadStudentData.html')

@app.route('/markattendance')
def markattendance():
    record1 = Student.query.filter_by(roll_no=current_user.username).first()
    u_name = record1.name
    email = record1.email
    print(u_name)
    return render_template('markAttendance.html',email=email,u_name=u_name)
    # return render_template('generate_otp.html', email=email)

@socketio.on('load_lectures')
def handle_load_lectures(data):
    print("Here")
    selected_day = data['selectedDay']
    print(selected_day)
    selected_batch = data['selectedBatch']
    print(selected_batch)
    if(selected_batch=="Lecture"):
        slots_data = TimeTable.query.filter_by(batch='1', day=selected_day).first()
        # Check if slots_data is not None to avoid errors
        if slots_data:
            print("Here i Am")
            # Iterate through each attribute of the record
            for attr, value in vars(slots_data).items():
                value_str = str(value)
                if '[PR]' in value_str:
                    # If it contains '[PR]', replace the value with an empty string
                    setattr(slots_data, attr, value_str.replace(value_str, '-'))
    else:    
        # Use SQLAlchemy to query the database
        slots_data = TimeTable.query.filter_by(batch=selected_batch, day=selected_day).first()
        if slots_data:
            print("Here i Am")
            # Iterate through each attribute of the record
            for attr_name in slots_data.__table__.columns.keys():
                # Get the value of the attribute
                value = getattr(slots_data, attr_name)
                # Convert the value to a string
                value_str = str(value)
                if '[PR]' not in value_str:
                    # If it doesn't contain '[PR]', replace the value with '-'
                    setattr(slots_data, attr_name, '-')
    # Convert the result to a dictionary for sending over Socket.IO
    slots_data_dict = {
        'slot1': slots_data.slot1,
        'slot2': slots_data.slot2,
        'slot3': slots_data.slot3,
        'slot4': slots_data.slot4,
        'slot5': slots_data.slot5
    }
    # Emit the response back to the client
    slots_data_list = list(slots_data_dict.values())
    for item in slots_data_list:
        print(item)
    socketio.emit('lectures_loaded', slots_data_list)

@app.route("/showAttendance", methods = ['POST'])
@login_required
def showAttendance():
    # try:   
    #     selected_day_str = request.form['selectedDay']
    #     selected_day = datetime.strptime(selected_day_str, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")  
    #     dte = selected_day.strftime("%A, %d %B %Y")
    #     selected_batch = request.form['selectedBatch']
    #     if(selected_batch == "Lecture"):
    #         selected_batch='L'
    #     selected_slot = request.form['selectedSlot']
    #     print(selected_day.date(),selected_batch,selected_slot)
    #     attendanceRecord = AttendanceRecord.query.filter_by(date=selected_day.date(), batch=selected_batch, slot=selected_slot).order_by(AttendanceRecord.roll_no).all()
    #     attendance_data = []
    #     for record in attendanceRecord:
    #         attendance_data.append({
    #             'roll_no': record.roll_no,
    #             'name': record.name,
    #             'email': record.email,
    #             'present': record.present
    #             # Add more fields as needed
    #         })
    #     count = len(attendance_data)
    #     print(attendance_data)
    #     if(selected_batch == "L"):
    #         selected_batch="Lecture"
    #     elif(selected_batch=="1"):
    #         selected_batch="IF1"
    #     elif(selected_batch=="2"):
    #         selected_batch="IF2"
    #     elif(selected_batch=="3"):
    #         selected_batch="IF3"
    #     # result = AttendanceRecord.query.with_entities(AttendanceRecord.date, AttendanceRecord.subject, AttendanceRecord.batch).first()
    # except Exception as e:
    #     return jsonify({'error': 'An error occurred while fetching attendance data'})
    #     return []
    # print(attendance_data,count,dte, selected_batch, selected_slot)
    # return jsonify({'attendance': attendance_data,'count': count, 'selected_day':dte,'selected_batch':selected_batch,'selected_slot':selected_slot})
    return render_template('generate_otp.html')
@app.route("/fetchAttendance")
@login_required
def fetchAttendance():
    return render_template('fetchAttendance.html')

@app.route("/fetch_marked_attendance",methods = ['POST'])
@login_required
def handle_fetch_marked_attendance():
    try:   
        selected_day_str = request.form['selectedDay']
        selected_day = datetime.strptime(selected_day_str, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")  
        print(selected_day.date())
        attendance_records = markedAttendance.query.filter_by(date=selected_day.date()).with_entities(markedAttendance.batch, markedAttendance.slot).all()
        unique_records = set((record.batch, record.slot) for record in attendance_records)
        print(unique_records)
        attendance_data = []
        for record in unique_records:
            attendance_data.append({
                'batch': record[0],
                'slot': record[1],
            })
            print(attendance_data)
        # result = AttendanceRecord.query.with_entities(AttendanceRecord.date, AttendanceRecord.subject, AttendanceRecord.batch).first()
    except Exception as e:
        return jsonify({'error': 'An error occurred while fetching attendance data'})
        return []
    return jsonify({'slots_batches': attendance_data})

@app.route('/upload_student_data', methods=['POST'])
def upload_student_data():
  if 'studentData' in request.files:
    student_data_file = request.files['studentData']
    df = pd.read_excel(student_data_file.stream)

    # Iterate through rows and add data to the 'students' table
    for index, row in df.iterrows():
      student = Student(
        roll_no=row['roll_no'],
        name=row['name'],
        email=row['email']
      )
      db.session.add(student)
    db.session.commit()

@app.route('/autocomplete')
def autocomplete():
    search_term = request.args.get('q')
    results = Student.query.filter(
        db.or_(
            Student.roll_no.like(f'%{search_term}%'),
            Student.name.like(f'%{search_term}%'),
            Student.email.like(f'%{search_term}%')
        )
    ).all()

    data = [{
        'roll_no': student.roll_no,
        'name': student.name,
        'email': student.email
    } for student in results]

    return jsonify(data)

#TESTER'S IMPLEMENTATION FOR OTP

# Route for the OTP generation page
# @app.route('/generate_otp', methods=['GET','POST'])
# def generate_otp():
#     if request.method == 'POST':
#         uname = current_user.username
#         batch = request.form.get('selectedBatch')
#         day = request.form.get('selectedDay')
#         slot = request.form.get('selectedSlot') 

#         session['batch'] = batch
#         session['day'] = day
#         session['slot'] = slot

#         record1 = Student.query.filter_by(roll_no=uname).first()
#         email = record1.email
#         otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
#         session['otp'] = otp  # Store OTP in session for verification
#         session['email'] = email  # Store email in session
        
#         # Create a message with subject and sender alias
#         msg = Message(
#             subject='Attendance System OTP Verification',  # Custom subject
#             sender=('Attendance System', 'hodkirmada@gmail.com'),  # Sender alias and actual email
#             recipients=[email]
#         )
#         msg.body = f'Your OTP is: {otp}'
#         print("HERE NOW!!!!")
#         try:
#             mail.send(msg)
#             print("HERE NOW 2 !!!!")
#             return redirect(url_for('attendance_success'))  
#         except Exception as e:
#             print(f"Error: {e}")


# @app.route('/isLocationVerified', methods=['POST'])
# def is_location_verified():
#     location_verified = session.get('location_flag', False)
#     if location_verified:
#         return redirect(url_for('generate_otp'), method='POST')
#     else:
#         return redirect(url_for('generate_otp'))



@app.route('/generate_otp', methods=['GET', 'POST'])
def generate_otp():
    record1 = Student.query.filter_by(roll_no=current_user.username).first()
    email = record1.email
    if request.method == 'POST':
        location_verified = session.get('location_flag', False)
        if not location_verified:
            return render_template('generate_otp.html', msg = "Location not verified, or outside the required region.",email=email)
        record1 = Student.query.filter_by(roll_no=current_user.username).first()
        email = record1.email
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
        session['otp'] = otp  # Store OTP in session for verification
        session['email'] = email  # Store email in session
        
        # Create a message with subject and sender alias
        msg = Message(
            subject='Attendance System OTP Verification',  # Custom subject
            sender=('Attendance System', 'attendance-admin@gmail.com'),  # Sender alias and actual email
            recipients=[email]
        )
        msg.body = f'Roll No: {current_user.username}\nYour OTP for marking the attendance is: {otp}.'
        
        try:
            mail.send(msg)
            flash('OTP sent to your email. Please check your inbox.', 'success')
            return redirect(url_for('verify_otp'))
        except Exception as e:
            flash('Failed to send OTP. Please try again.', 'danger')
            print(f"Error: {e}")
        
    
    return render_template('generate_otp.html', email=email)



# Route for the OTP verification page
# @app.route('/verify_otp', methods=['GET', 'POST'])
# def verify_otp():
#     if request.method == 'POST':
           
#         entered_otp = request.form['otp']
#         if entered_otp == session.get('otp'):
#             uname = current_user.username
#             batch = session.get('batch')
#             day = datetime.strptime(session.get('day'), "%Y-%m-%d").date()  # Parse date string to date object
#             slot = session.get('slot')
#             student_record = Student.query.filter_by(roll_no=uname).first()

#             # Insert into AttendanceRecord
#             new_attendance = AttendanceRecord(
#                 date=date,
#                 batch=batch,
#                 slot=slot,
#                 roll_no=uname,
#                 name=student_record.name,
#                 email=student_record.email,
#                 present='y'  # Mark as present
#             )
#             db.session.add(new_attendance)
#             db.session.commit()
#             session.pop('otp', None)  # Clear OTP from session after verification
#             return redirect(url_for('home'))
#         # else:
#             # flash('Invalid OTP. Please try again.', 'danger')       
#     return render_template('verify_otp.html')


@app.route('/submitAttendance', methods=['POST'])
def submitAttendance():
    record1 = Student.query.filter_by(roll_no=current_user.username).first()
    u_name = record1.name
    email = record1.email
    rollno = current_user.username
    batch = request.form.get('selectedBatch')
    date = request.form.get('selectedDay')
    slot = request.form.get('selectedSlot')
    # Insert into AttendanceRecord
    new_attendance = AttendanceRecord(
        date=datetime.fromisoformat(date),
        batch=batch,
        slot=slot,
        roll_no=rollno,
        name=u_name,
        email=email,
        present='y'  # Mark as present
    )
    db.session.add(new_attendance)
    db.session.commit()
    session.pop('otp_verified', None)
    session.pop('location_flag', None)
    flash('Attendance Marked Successfully!')
    return jsonify({'status': 'success', 'message': 'Attendance marked successfully'})

# Route for the OTP verification page
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session.get('otp'):
            session.pop('otp', None)  # Clear OTP from session after verification
            return redirect(url_for('attendance_success'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html')




# Dummy route to indicate successful attendance marking
@app.route('/attendance_success')
def attendance_success():
    session['otp_verified'] = True
    return render_template('success.html')

@app.route('/initVerifyLocation')
def initVerifyLocation():
    return render_template('verifyLocation.html')


@app.route('/verifyLocation', methods=['POST'])
def verify_location():
    try:
        # Get latitude and longitude from the request
        data = request.json
        user_lat = data.get('latitude')
        user_lon = data.get('longitude')
        
        if not user_lat or not user_lon:
            return jsonify({"error": "Latitude and Longitude are required!"}), 400

        user_coordinates = (float(user_lat), float(user_lon))

        # Calculate the distance in meters
        distance = geodesic(AISSMS_COORDINATES, user_coordinates).meters

        # Check if within 50 meters
        if distance <= 50:
            session['location_flag'] = True
            return jsonify({"status": "success", "message": "Within range, redirect to OTP page."})
        else:
            session['location_flag'] = False
            return jsonify({"status": "failed", "message": "Not within range."})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/fetch_lectures', methods=['POST'])
def fetch_lectures():
    # Get the selected day and batch from the AJAX request
    selected_day = request.form.get('selectedDay')
    selected_batch = request.form.get('selectedBatch')
    
    # Determine the current batch value
    if selected_batch == "Lecture":
        cur = '1'
    else:
        cur = selected_batch  # Assuming selected_batch can be '1', '2', or '3'

    timetable_entries = TimeTable.query.filter_by(day=selected_day, batch=cur).all()
    if not timetable_entries:
        return jsonify({"message": "No timetable found for the selected day and batch.", "slotsData": []}), 404

    # Prepare slots data for all matching entries
    slots_data = []
    for entry in timetable_entries:
        slots = []
        for i in range(1, 9):  # Assuming there are 8 slots (slot1 to slot8)
            slot_value = getattr(entry, f'slot{i}')
            if selected_batch == "Lecture":
                # Omit slots containing [ PR ]
                if "[PR]" not in slot_value:
                    slots.append(slot_value)
            else:
                # Append only slots containing [ PR ]
                if "[PR]" in slot_value:
                    slots.append(slot_value)

        # Append the filtered slots to the slots_data
        slots_data.append(slots)

    # Return the data in JSON format
    return jsonify({"slotsData": slots_data}), 200


if __name__ == "__main__":
    app.run(debug=True)