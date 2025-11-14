from app import app, Student, Attendance, Grade

def test_attendance_data():
    with app.app_context():
        # Test student data
        student = Student.query.filter_by(student_id='STU000001').first()
        print(f"Student: {student.first_name} {student.last_name}")
        
        # Test attendance data  
        attendance = Attendance.query.filter_by(student_id=student.id).all()
        print(f"Total attendance records: {len(attendance)}")
        
        present = [a for a in attendance if a.status == "present"]
        absent = [a for a in attendance if a.status == "absent"]
        late = [a for a in attendance if a.status == "late"]
        excused = [a for a in attendance if a.status == "excused"]
        
        print(f"Present days: {len(present)}")
        print(f"Absent days: {len(absent)}")
        print(f"Late days: {len(late)}")
        print(f"Excused days: {len(excused)}")
        print(f"Attendance percentage: {len(present)/len(attendance)*100:.1f}%" if attendance else "0%")
        
        # Test grades data
        grades = Grade.query.filter_by(student_id=student.id).all()
        print(f"Total grades: {len(grades)}")
        if grades:
            for grade in grades:
                print(f"Subject: {grade.subject.name if grade.subject else 'Unknown'}, Grade: {grade.grade_value}")

if __name__ == "__main__":
    test_attendance_data()