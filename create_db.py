from app import app, db, Authenticate, TeacherMap, Student, bcrypt, AttendanceRecord, TimeTable, markedAttendance
import pandas as pd
# Create an application context
with app.app_context():
    try:
        # Create the database and the db table
        db.create_all()

        # Use session.no_autoflush context manager to disable autoflush temporarily
        
        # Use session.no_autoflush context manager to disable autoflush temporarily
        with db.session.no_autoflush:
            
            df = pd.read_excel('student_data.xlsx')
            # Insert user data
            df = pd.read_excel('student_data.xlsx')
            for index, row in df.iterrows():
                authenticate = Authenticate(
                    username=row['roll_no'],
                    password=row['roll_no'],
                    role = row['role']
                )
                db.session.add(authenticate)
            
            authenticate1 = Authenticate(
                    username='sssonawane',
                    password='sunil123',
                    role = 'admin'
                )
            authenticate2 = Authenticate(
                    username='vrpalandurkar',
                    password='varsha123',
                    role = 'admin'
                )
            authenticate3 = Authenticate(
                    username='askhandagale',
                    password='anjali123',
                    role = 'admin'
                )
            authenticate4 = Authenticate(
                    username='vvshetkar',
                    password='vishal123',
                    role = 'admin'
                )
            authenticate5 = Authenticate(
                    username='rbgurav',
                    password='rohini123',
                    role = 'admin'
                )
            db.session.add(authenticate1)
            db.session.add(authenticate2)
            db.session.add(authenticate3)
            db.session.add(authenticate4)
            db.session.add(authenticate5)
            # commit the changes without autoflush
            db.session.commit()

            map1 = TeacherMap(
                teacherName = "sssonawane",
                subject = 'EST'
            )
            map2 = TeacherMap(
                teacherName = "vrpalandurkar",
                subject = 'CSS'
            )
            map3 = TeacherMap(
                teacherName = "askhandagale",
                subject = 'OSY'
            )
            map4 = TeacherMap(
                teacherName = "vvshetkar",
                subject = 'EDE'
            )
            map5 = TeacherMap(
                teacherName = "rbgurav",
                subject = 'DMA'
            )
            # Insert student data
            db.session.add(map1)
            db.session.add(map2)
            db.session.add(map3)
            db.session.add(map4)
            db.session.add(map5)


    # Iterate through rows and add data to the 'students' table
            for index, row in df.iterrows():
                student = Student(
                    roll_no=row['roll_no'],
                    name=row['name'],
                    email = row['email'],
                    batch = row['batch'],
                    phone_no = row['phone_no']
                )
                db.session.add(student)

            df = pd.read_excel('TimeTable.xlsx')

    # Iterate through rows and add data to the 'students' table
            for index, row in df.iterrows():
                tb= TimeTable(
                    batch = row['batch'],
                    day = row['day'],
                    slot1 = row['slot1'],
                    slot2 = row['slot2'],
                    slot3 = row['slot3'],
                    slot4 = row['slot4'],
                    slot5 = row['slot5'],
                    slot6 = row['slot6'],
                    slot7 = row['slot7'],
                    slot8 = row['slot8'],
                )
                db.session.add(tb)

            db.session.commit()

    except Exception as e:
        print(f"Error during database creation: {e}")