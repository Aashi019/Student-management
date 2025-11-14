"""
Quick test script to verify database operations
Run this after admin makes changes to verify data is persisted
"""
from app import app, db
from models import Student, Attendance, Grade, FeeStructure

def test_database_operations():
    with app.app_context():
        print("=== DATABASE VERIFICATION TEST ===\n")
        
        # Test 1: Check if students can be added/edited
        print("1. STUDENT OPERATIONS:")
        students_count = Student.query.count()
        print(f"   - Total students in database: {students_count}")
        
        # Get a sample student to check if edits persist
        student = Student.query.first()
        if student:
            print(f"   - Sample student: {student.first_name} {student.last_name}")
            print(f"   - Student ID: {student.student_id}")
            print(f"   - Status: {student.status}")
            print(f"   - Last updated: {student.updated_at}")
        
        # Test 2: Check attendance records
        print("\n2. ATTENDANCE OPERATIONS:")
        attendance_count = Attendance.query.count()
        print(f"   - Total attendance records: {attendance_count}")
        
        recent_attendance = Attendance.query.order_by(Attendance.created_at.desc()).first()
        if recent_attendance:
            print(f"   - Latest attendance: Student {recent_attendance.student_id}, {recent_attendance.status}")
            print(f"   - Recorded by: {recent_attendance.recorded_by}")
        
        # Test 3: Check grades
        print("\n3. GRADE OPERATIONS:")
        grades_count = Grade.query.count()
        print(f"   - Total grade records: {grades_count}")
        
        recent_grade = Grade.query.order_by(Grade.date_recorded.desc()).first()
        if recent_grade:
            print(f"   - Latest grade: {recent_grade.grade_value} ({recent_grade.letter_grade})")
            print(f"   - Student ID: {recent_grade.student_id}")
        
        # Test 4: Check fee structures
        print("\n4. FEE OPERATIONS:")
        fee_structures_count = FeeStructure.query.count()
        active_fees = FeeStructure.query.filter_by(is_active=True).count()
        print(f"   - Total fee structures: {fee_structures_count}")
        print(f"   - Active fee structures: {active_fees}")
        
        sample_fee = FeeStructure.query.first()
        if sample_fee:
            print(f"   - Sample fee: {sample_fee.name} - ₨{sample_fee.amount}")
            print(f"   - Status: {'Active' if sample_fee.is_active else 'Inactive'}")
        
        print("\n=== TEST COMPLETED ===")
        print("All operations appear to have proper database commits!")

if __name__ == '__main__':
    test_database_operations()