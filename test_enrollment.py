from app import app, Student, Enrollment
from models import Subject

with app.app_context():
    student = Student.query.filter_by(student_id='STU000001').first()
    print(f"Student: {student.first_name} {student.last_name}")
    
    enrollment = student.enrollments.first()
    if enrollment:
        print(f"Faculty: {enrollment.subject.name}")
        print(f"Subject Code: {enrollment.subject.code}")
    else:
        print("No enrollment found")
        
    # Show all enrollments for debugging
    enrollments = student.enrollments.all()
    print(f"Total enrollments: {len(enrollments)}")
    for e in enrollments:
        print(f"  - {e.subject.name} ({e.subject.code})")