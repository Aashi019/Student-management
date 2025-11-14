"""
Sample data creation script for the Student Management System
"""
from app import app, db
from models import User, Student, Subject, Grade, Attendance, AcademicYear, Enrollment, Event, FeeStructure, FeePayment, FeeReceipt
from datetime import datetime, date, timedelta
import random

def create_sample_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # Create admin user
        admin = User(username='admin', email='admin@school.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create teacher users
        teacher1 = User(username='teacher1', email='teacher1@school.com', role='teacher')
        teacher1.set_password('teacher123')
        db.session.add(teacher1)
        
        teacher2 = User(username='teacher2', email='teacher2@school.com', role='teacher')
        teacher2.set_password('teacher123')
        db.session.add(teacher2)
        
        # Create student user for login
        student_user = User(username='student', email='student@school.com', role='student')
        student_user.set_password('student123')
        db.session.add(student_user)
        
        # Create a corresponding Student record for the login user
        login_student = Student(
            student_id='STU999999',
            first_name='Student',
            last_name='Portal',
            email='student@school.com',  # Must match the User email for linking
            phone='981-123456',
            date_of_birth=date(2002, 1, 15),
            gender='female',
            address='Student Address, Kathmandu',
            city='Kathmandu',
            state='Bagmati',
            zip_code='44600',
            emergency_contact='Student Parent',
            emergency_phone='981-654321',
            grade_level='2nd Year',
            enrollment_date=date(2024, 8, 15),
            graduation_year=2027,
            status='active',
            gpa=3.5
        )
        login_student.set_password('student123')
        db.session.add(login_student)
        
        # Create faculties (instead of subjects)
        faculties_data = [
            {'name': 'Bachelor of Science in Computer Science and Information Technology', 'code': 'BSC-CSIT', 'credits': 120, 'department': 'Computer Science'},
            {'name': 'Bachelor of Computer Applications', 'code': 'BCA', 'credits': 96, 'department': 'Computer Applications'}
        ]
        
        subjects = []
        for faculty_data in faculties_data:
            subject = Subject(**faculty_data)
            subjects.append(subject)
            db.session.add(subject)
        
        # Create academic year
        academic_year = AcademicYear(
            year='2024-25',
            start_date=date(2024, 8, 1),
            end_date=date(2025, 7, 31),
            is_current=True
        )
        db.session.add(academic_year)
        
        # Create sample students with Nepali names (only 10 students)
        students_data = [
            {'first_name': 'Aashi', 'last_name': 'Sharma', 'email': 'aashi.sharma@student.school.com', 'grade_level': '1st Year', 'gender': 'female', 'faculty': 'BSC-CSIT'},
            {'first_name': 'Rohan', 'last_name': 'Thapa', 'email': 'rohan.thapa@student.school.com', 'grade_level': '2nd Year', 'gender': 'male', 'faculty': 'BCA'},
            {'first_name': 'Priya', 'last_name': 'Gurung', 'email': 'priya.gurung@student.school.com', 'grade_level': '1st Year', 'gender': 'female', 'faculty': 'BSC-CSIT'},
            {'first_name': 'Sagar', 'last_name': 'Bhandari', 'email': 'sagar.bhandari@student.school.com', 'grade_level': '3rd Year', 'gender': 'male', 'faculty': 'BCA'},
            {'first_name': 'Anita', 'last_name': 'Rai', 'email': 'anita.rai@student.school.com', 'grade_level': '2nd Year', 'gender': 'female', 'faculty': 'BSC-CSIT'},
            {'first_name': 'Bibek', 'last_name': 'Karki', 'email': 'bibek.karki@student.school.com', 'grade_level': '1st Year', 'gender': 'male', 'faculty': 'BCA'},
            {'first_name': 'Sunita', 'last_name': 'Shrestha', 'email': 'sunita.shrestha@student.school.com', 'grade_level': '4th Year', 'gender': 'female', 'faculty': 'BSC-CSIT'},
            {'first_name': 'Kiran', 'last_name': 'Adhikari', 'email': 'kiran.adhikari@student.school.com', 'grade_level': '3rd Year', 'gender': 'male', 'faculty': 'BCA'},
            {'first_name': 'Sneha', 'last_name': 'Poudel', 'email': 'sneha.poudel@student.school.com', 'grade_level': '2nd Year', 'gender': 'female', 'faculty': 'BSC-CSIT'},
            {'first_name': 'Rajesh', 'last_name': 'Tamang', 'email': 'rajesh.tamang@student.school.com', 'grade_level': '4th Year', 'gender': 'male', 'faculty': 'BCA'}
        ]
        
        students = []
        for i, student_data in enumerate(students_data, 1):
            # Calculate age based on university year (18-22 years old)
            year_mapping = {'1st Year': 18, '2nd Year': 19, '3rd Year': 20, '4th Year': 21}
            age = year_mapping.get(student_data['grade_level'], 19)
            birth_year = datetime.now().year - age
            
            # Set different statuses for different students
            if i in [2, 5, 8]:  # Students 2, 5, and 8 will have different statuses
                if i == 2:
                    student_status = 'inactive'
                elif i == 5:
                    student_status = 'suspended'
                else:  # i == 8
                    student_status = 'graduated'
            else:
                student_status = 'active'
            
            student = Student(
                student_id=f"STU{i:06d}",
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                email=student_data['email'],
                phone=f"98{random.randint(10, 99)}-{random.randint(100000, 999999)}",
                date_of_birth=date(birth_year, random.randint(1, 12), random.randint(1, 28)),
                gender=student_data['gender'],
                address=f"{random.choice(['Thamel', 'Basantapur', 'Patan', 'Bhaktapur', 'Boudha', 'Swayambhu', 'Baneshwor'])}-{random.randint(1, 50)}",
                city=random.choice(['Kathmandu', 'Lalitpur', 'Bhaktapur', 'Pokhara', 'Biratnagar']),
                state=random.choice(['Bagmati', 'Gandaki', 'Lumbini', 'Province 1', 'Koshi']),
                zip_code=f"44{random.randint(100, 699)}",
                emergency_contact=f"{student_data['first_name']} Parent",
                emergency_phone=f"98{random.randint(10, 99)}-{random.randint(100000, 999999)}",
                grade_level=student_data['grade_level'],
                enrollment_date=date(2024, 8, random.randint(15, 31)),
                graduation_year=2024 + (5 - int(student_data['grade_level'][0])),  # 4-year program
                status=student_status,
                gpa=round(random.uniform(2.5, 4.0), 2)
            )
            # Set password for student portal (password = "student" + student number)
            student.set_password(f"student{i}")
            students.append(student)
            db.session.add(student)
            
        db.session.commit()
        
        # Create sample grades - ensuring at least one failing grade per faculty
        grade_letters = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F', 'F']
        grade_values = [95, 90, 87, 83, 80, 77, 73, 70, 67, 63, 45, 35]
        
        # Map student data to students for faculty assignment
        student_faculty_map = {student.id: students_data[i]['faculty'] for i, student in enumerate(students)}
        
        # Semester numbering based on year level (1st, 2nd, 3rd, etc.)
        semester_mapping = {
            '1st Year': ['1st', '2nd'],
            '2nd Year': ['3rd', '4th'],
            '3rd Year': ['5th', '6th'],
            '4th Year': ['7th', '8th']
        }
        
        # Separate students by faculty
        bsc_csit_students = []
        bca_students = []
        
        for i, student in enumerate(students):
            student_faculty = student_faculty_map[student.id]
            if student_faculty == 'BSC-CSIT':
                bsc_csit_students.append(student)
            else:
                bca_students.append(student)
        
        # Create grades ensuring at least one failing grade per faculty
        for faculty_students, faculty_code in [(bsc_csit_students, 'BSC-CSIT'), (bca_students, 'BCA')]:
            # Find the corresponding subject (faculty)
            faculty_subject = None
            for subject in subjects:
                if subject.code == faculty_code:
                    faculty_subject = subject
                    break
            
            if faculty_subject and faculty_students:
                # Ensure at least one student gets a failing grade (F)
                failing_student_idx = 0  # First student in each faculty gets failing grade
                
                for idx, student in enumerate(faculty_students):
                    # Get appropriate semester based on student's year level
                    possible_semesters = semester_mapping.get(student.grade_level, ['1st'])
                    semester = random.choice(possible_semesters)
                    
                    if idx == failing_student_idx:
                        # Force failing grade for first student in each faculty
                        grade_idx = len(grade_letters) - 1 - random.randint(0, 1)  # F grade (45 or 35)
                        grade_value = grade_values[grade_idx]
                        letter_grade = 'F'
                        print(f"Creating failing grade for {student.first_name} {student.last_name} in {faculty_code}: {grade_value}% (F)")
                    else:
                        # Normal random grades for other students
                        grade_idx = random.randint(0, len(grade_letters) - 3)  # Exclude the two F grades for others
                        grade_value = grade_values[grade_idx] + random.randint(-3, 3)
                        letter_grade = grade_letters[grade_idx]
                    
                    grade = Grade(
                        student_id=student.id,
                        subject_id=faculty_subject.id,
                        grade_value=max(0, grade_value),  # Ensure grade doesn't go below 0
                        letter_grade=letter_grade,
                        grade_type='semester_exam',
                        semester=semester,
                        academic_year='2024-25',
                        date_recorded=date.today() - timedelta(days=random.randint(1, 60))
                    )
                    db.session.add(grade)
        
        # Create enrollments for students in their respective faculties
        for i, student in enumerate(students):
            # Get student's faculty
            student_faculty = student_faculty_map[student.id]
            
            # Find the corresponding subject (faculty)
            faculty_subject = None
            for subject in subjects:
                if subject.code == student_faculty:
                    faculty_subject = subject
                    break
            
            if faculty_subject:
                # Create enrollment
                enrollment = Enrollment(
                    student_id=student.id,
                    subject_id=faculty_subject.id,
                    semester='1st',
                    academic_year='2024-25',
                    enrollment_date=date(2024, 8, random.randint(15, 31)),
                    status='enrolled'
                )
                db.session.add(enrollment)
        
        db.session.commit()
        
        # Create sample attendance records
        start_date = date(2024, 8, 15)
        end_date = date.today()
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                for student in students:
                    # 95% chance of being present
                    status = 'present' if random.random() < 0.95 else random.choice(['absent', 'late', 'excused'])
                    
                    # Determine period based on student's faculty
                    student_faculty = student_faculty_map[student.id]
                    if student_faculty == 'BCA':
                        period = 'morning'
                    else:  # BSC-CSIT
                        period = 'day'
                    
                    attendance = Attendance(
                        student_id=student.id,
                        date=current_date,
                        status=status,
                        period=period
                    )
                    db.session.add(attendance)
            
            current_date += timedelta(days=1)
        
        # Create sample events
        today = date.today()
        events_data = [
            {
                'title': 'University Orientation Program',
                'description': 'Welcome orientation for new students joining BSC-CSIT and BCA programs.',
                'event_date': datetime.combine(today + timedelta(days=3), datetime.min.time().replace(hour=9)),
                'end_date': datetime.combine(today + timedelta(days=3), datetime.min.time().replace(hour=17)),
                'event_type': 'orientation',
                'location': 'Main Auditorium',
                'color': '#10b981'
            },
            {
                'title': 'Mid-Semester Examination',
                'description': 'Mid-semester examinations for all programs.',
                'event_date': datetime.combine(today + timedelta(days=10), datetime.min.time().replace(hour=10)),
                'end_date': datetime.combine(today + timedelta(days=15), datetime.min.time().replace(hour=16)),
                'event_type': 'exam',
                'location': 'Examination Hall',
                'color': '#dc2626'
            },
            {
                'title': 'Computer Science Workshop',
                'description': 'Hands-on workshop on modern web development technologies.',
                'event_date': datetime.combine(today + timedelta(days=7), datetime.min.time().replace(hour=14)),
                'end_date': datetime.combine(today + timedelta(days=7), datetime.min.time().replace(hour=18)),
                'event_type': 'workshop',
                'location': 'Computer Lab',
                'color': '#3b82f6'
            },
            {
                'title': 'Sports Day',
                'description': 'Annual sports day with various competitions and activities.',
                'event_date': datetime.combine(today + timedelta(days=21), datetime.min.time().replace(hour=8)),
                'end_date': datetime.combine(today + timedelta(days=21), datetime.min.time().replace(hour=17)),
                'event_type': 'sports',
                'location': 'Sports Ground',
                'color': '#f59e0b'
            },
            {
                'title': 'Career Fair 2025',
                'description': 'Career fair with leading IT companies for final year students.',
                'event_date': datetime.combine(today + timedelta(days=30), datetime.min.time().replace(hour=10)),
                'end_date': datetime.combine(today + timedelta(days=30), datetime.min.time().replace(hour=16)),
                'event_type': 'career',
                'location': 'Convention Center',
                'color': '#8b5cf6'
            },
            {
                'title': 'Final Semester Examination',
                'description': 'Final semester examinations for all programs.',
                'event_date': datetime.combine(today + timedelta(days=45), datetime.min.time().replace(hour=9)),
                'end_date': datetime.combine(today + timedelta(days=60), datetime.min.time().replace(hour=17)),
                'event_type': 'exam',
                'location': 'Examination Hall',
                'color': '#dc2626'
            },
            {
                'title': 'Graduation Ceremony',
                'description': 'Graduation ceremony for completing students.',
                'event_date': datetime.combine(today + timedelta(days=75), datetime.min.time().replace(hour=10)),
                'end_date': datetime.combine(today + timedelta(days=75), datetime.min.time().replace(hour=15)),
                'event_type': 'ceremony',
                'location': 'Main Campus',
                'color': '#059669'
            }
        ]
        
        # Add past events for demonstration
        past_events_data = [
            {
                'title': 'Welcome Assembly',
                'description': 'Welcome assembly for the new academic year.',
                'event_date': datetime.combine(today - timedelta(days=30), datetime.min.time().replace(hour=10)),
                'event_type': 'assembly',
                'location': 'Main Auditorium',
                'color': '#6366f1'
            },
            {
                'title': 'First Year Orientation',
                'description': 'Orientation program for first-year students.',
                'event_date': datetime.combine(today - timedelta(days=25), datetime.min.time().replace(hour=9)),
                'event_type': 'orientation',
                'location': 'Conference Hall',
                'color': '#10b981'
            }
        ]
        
        # Create events
        all_events = events_data + past_events_data
        admin_user = User.query.filter_by(username='admin').first()
        
        for event_data in all_events:
            event = Event(
                title=event_data['title'],
                description=event_data['description'],
                event_date=event_data['event_date'],
                end_date=event_data.get('end_date'),
                event_type=event_data['event_type'],
                location=event_data['location'],
                color=event_data['color'],
                created_by=admin_user.id if admin_user else None
            )
            db.session.add(event)
        
        db.session.commit()
        
        # Create Fee Structures
        print("Creating fee structures...")
        
        # Simplified fee structure with only 3 fee types, different amounts for each faculty
        # BSC-CSIT (higher fees) vs BCA (lower fees)
        fee_structures = []
        
        for subject in subjects:  # For each faculty
            if subject.code == 'BSC-CSIT':
                # Higher fees for BSC-CSIT
                fees_data = [
                    {'name': 'Tuition Fee', 'amount': 78000, 'fee_type': 'semester'},
                    {'name': 'Lab Fee', 'amount': 12000, 'fee_type': 'semester'},
                    {'name': 'Registration Fee', 'amount': 5000, 'fee_type': 'one-time'},
                ]
            else:  # BCA
                # Lower fees for BCA
                fees_data = [
                    {'name': 'Tuition Fee', 'amount': 65000, 'fee_type': 'semester'},
                    {'name': 'Lab Fee', 'amount': 8000, 'fee_type': 'semester'},
                    {'name': 'Registration Fee', 'amount': 3000, 'fee_type': 'one-time'},
                ]
            
            # Create fee structures only for current semester (1st semester)
            current_semester = '1st'
            due_date = date(2024, 8, 1) + timedelta(days=30)
            
            for fee_data in fees_data:
                fee_structure = FeeStructure(
                    name=fee_data['name'],
                    description=f"{fee_data['name']} for {subject.name} - {current_semester} Semester",
                    amount=fee_data['amount'],
                    fee_type=fee_data['fee_type'],
                    faculty_id=subject.id,
                    semester=current_semester,
                    academic_year='2024-25',
                    due_date=due_date
                )
                fee_structures.append(fee_structure)
                db.session.add(fee_structure)
        
        db.session.commit()
        
        # Create Fee Payments for students
        print("Creating fee payments...")
        
        payment_methods = ['bank_transfer', 'cash', 'online', 'card']
        
        for student in students:
            # Get student's faculty
            student_faculty = student_faculty_map[student.id]
            
            # Find the corresponding subject (faculty)
            faculty_subject = None
            for subject in subjects:
                if subject.code == student_faculty:
                    faculty_subject = subject
                    break
            
            if faculty_subject:
                # Determine current semester for the student (simplified to 1st semester)
                current_semester = '1st'
                
                # Get fee structures for this student's faculty and current semester
                applicable_fees = [fs for fs in fee_structures 
                                 if fs.faculty_id == faculty_subject.id and 
                                 fs.semester == current_semester]
                
                # Create payments for some fees (simulate partial payments and unpaid fees)
                # Ensure 2-3 students have unpaid/partial fees
                students_with_pending = []
                if student.student_id in ['STU000003', 'STU000007', 'STU000009']:
                    students_with_pending.append(student.student_id)
                
                for i, fee_structure in enumerate(applicable_fees):
                    payment_made = True
                    payment_percentage = 1.0  # Default to full payment
                    
                    # Special handling for students who should have pending fees
                    if student.student_id in ['STU000003', 'STU000007', 'STU000009']:
                        if student.student_id == 'STU000003':
                            # Student 3: Has paid tuition fully, lab fee partially, registration not paid
                            if fee_structure.name == 'Tuition Fee':
                                payment_percentage = 1.0  # Full payment
                            elif fee_structure.name == 'Lab Fee':
                                payment_percentage = 0.5   # Half payment
                            else:  # Registration Fee
                                payment_made = False       # No payment
                        elif student.student_id == 'STU000007':
                            # Student 7: Has paid registration only, other fees unpaid
                            if fee_structure.name == 'Registration Fee':
                                payment_percentage = 1.0  # Full payment
                            else:
                                payment_made = False       # No payment for tuition and lab
                        elif student.student_id == 'STU000009':
                            # Student 9: Has paid tuition partially, other fees unpaid
                            if fee_structure.name == 'Tuition Fee':
                                payment_percentage = 0.6   # 60% payment
                            else:
                                payment_made = False       # No payment for lab and registration
                    else:
                        # For other students, mostly full payments with occasional partial payments
                        payment_chance = random.random()
                        if payment_chance < 0.9:  # 90% chance of payment
                            payment_percentage = random.choice([1.0, 1.0, 1.0, 1.0, 0.8, 0.9])  # Mostly full payments
                        else:
                            payment_made = False  # 10% chance of no payment
                    
                    if payment_made:
                        amount_to_pay = fee_structure.amount * payment_percentage
                        
                        # Generate unique receipt number
                        receipt_number = f"REC{student.id:04d}{fee_structure.id:04d}{random.randint(100, 999)}"
                        
                        payment = FeePayment(
                            student_id=student.id,
                            fee_structure_id=fee_structure.id,
                            amount_paid=amount_to_pay,
                            payment_date=date.today() - timedelta(days=random.randint(1, 90)),
                            payment_method=random.choice(payment_methods),
                            transaction_id=f"TXN{random.randint(100000, 999999)}",
                            receipt_number=receipt_number,
                            payment_status='completed',
                            recorded_by=admin_user.id if admin_user else None
                        )
                        db.session.add(payment)
        
        db.session.commit()
        
        print(f"Sample data created successfully!")
        print(f"- {len(students)} students with varied statuses:")
        print(f"  STU000001: Active, STU000002: Inactive")
        print(f"  STU000003: Active, STU000004: Active, STU000005: Suspended")
        print(f"  STU000006: Active, STU000007: Active, STU000008: Graduated")
        print(f"  STU000009: Active, STU000010: Active")
        print(f"- {len(subjects)} faculties (BSC-CSIT, BCA)")
        print(f"- Exactly 10 grades (1 per student) with at least 1 failing grade per faculty")
        print(f"- Attendance records with faculty-based periods:")
        print(f"  BCA students: Morning period")
        print(f"  BSC-CSIT students: Day period")
        print(f"- {len(all_events)} events (upcoming and past)")
        print(f"- {len(fee_structures)} fee structures:")
        print(f"  BSC-CSIT: Tuition ₨78,000, Lab ₨12,000, Registration ₨5,000")
        print(f"  BCA: Tuition ₨65,000, Lab ₨8,000, Registration ₨3,000")
        print(f"- Fee payments created with specific pending scenarios:")
        print(f"  STU000003: Tuition paid, Lab 50% paid, Registration unpaid")
        print(f"  STU000007: Only Registration paid, Tuition & Lab unpaid")
        print(f"  STU000009: Tuition 60% paid, Lab & Registration unpaid")
        print(f"- Admin user: admin / admin123")
        print(f"- Teacher users: teacher1 / teacher123, teacher2 / teacher123")
        print(f"- Student users: STU000001 / student1, STU000002 / student2, etc.")

if __name__ == '__main__':
    create_sample_data()
