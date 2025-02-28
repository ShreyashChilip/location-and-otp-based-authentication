from app import app, db, Authenticate, TeacherMap, Student, bcrypt, AttendanceRecord, TimeTable, markedAttendance
import pandas as pd


def recreate_table():
    with app.app_context():
        # Drop the TeacherMap table if it exists
        AttendanceRecord.__table__.drop(db.engine,checkfirst=True)
        AttendancePost.__table__.drop(db.engine,checkfirst=True)

        # Create the TeacherMap table
        AttendanceRecord.__table__.create(db.engine)
        AttendancePost.__table__.create(db.engine)
        print(" recreated successfully")

# Create an application context
with app.app_context():
    try:
        # Create all tables except TeacherMap (if not already created)
        db.create_all()

        # Recreate only TeacherMap table
        recreate_teacher_map_table()

        # Populate Authenticate and Student from student_data.xlsx
        df_students = pd.read_excel('student_data.xlsx')
        for index, row in df_students.iterrows():
            authenticate = Authenticate(
                username=row['roll_no'],
                password=row['roll_no'],  # Consider hashing with bcrypt
                role=row['role']
            )
            student = Student(
                roll_no=row['roll_no'],
                name=row['name'],
                email=row['email'],
                batch=row['batch'],
                phone_no='+91' + str(row['phone_no'])
            )
            db.session.add(authenticate)
            db.session.add(student)

        # Hardcoded admin users
        admins = [
            ("sssonawane", "sunil123", "admin"),
            ("vrpalandurkar", "varsha123", "admin"),
            ("askhandagale", "anjali123", "admin"),
            ("vvshetkar", "vishal123", "admin"),
            ("rbgurav", "rohini123", "admin")
        ]
        for username, password, role in admins:
            auth = Authenticate(
                username=username,
                password=password,  # Consider hashing with bcrypt
                role=role
            )
            db.session.add(auth)

        # Populate TimeTable from TimeTable.xlsx
        df_timetable = pd.read_excel('TimeTable.xlsx')
        for index, row in df_timetable.iterrows():
            tb = TimeTable(
                batch=row['batch'],
                day=row['day'],
                slot1=row['slot1'],
                slot2=row['slot2'],
                slot3=row['slot3'],
                slot4=row['slot4'],
                slot5=row['slot5'],
                slot6=row['slot6'],
                slot7=row['slot7'],
                slot8=row['slot8'],
            )
            db.session.add(tb)

        # Commit all changes
        db.session.commit()
        print("Database populated successfully (excluding initial TeacherMap data)")

    except Exception as e:
        db.session.rollback()
        print(f"Error during database creation: {e}")