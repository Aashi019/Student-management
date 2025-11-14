from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='admin')  # admin, teacher, staff
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    events_created = db.relationship('Event', backref='creator', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'is_active': self.is_active
        }

class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = (
        Index('idx_student_name', 'last_name', 'first_name'),
        Index('idx_student_status', 'status'),
        Index('idx_student_grade', 'grade_level'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))  # For student portal login
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(120))
    grade_level = db.Column(db.String(20), nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    graduation_year = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active', index=True)  # active, inactive, graduated, transferred
    gpa = db.Column(db.Float, default=0.0)
    photo_filename = db.Column(db.String(255))
    medical_info = db.Column(db.Text)  # Medical conditions or allergies
    notes = db.Column(db.Text)  # Additional notes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    grades = db.relationship('Grade', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def set_password(self, password):
        """Set password hash for student portal login"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password for student portal login"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Return student_id for Flask-Login (prefixed with 'student_')"""
        return f"student_{self.id}"
    
    def calculate_gpa(self):
        """Calculate current GPA based on grades"""
        grades = self.grades.filter(Grade.grade_value.isnot(None)).all()
        if not grades:
            return 0.0
        total = sum(g.grade_value for g in grades)
        return round(total / len(grades) / 25, 2)  # Convert to 4.0 scale
    
    def get_attendance_rate(self, days=30):
        """Calculate attendance rate for last N days"""
        from datetime import timedelta
        start_date = datetime.now().date() - timedelta(days=days)
        records = self.attendance_records.filter(Attendance.date >= start_date).all()
        if not records:
            return 0
        present = len([r for r in records if r.status == 'present'])
        return round((present / len(records)) * 100, 1)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'grade_level': self.grade_level,
            'gpa': self.gpa,
            'status': self.status,
            'photo_filename': self.photo_filename
        }

class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    qualification = db.Column(db.String(200))
    hire_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')
    photo_filename = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='teacher_profile', uselist=False)
    subjects_taught = db.relationship('SubjectTeacher', backref='teacher', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'full_name': self.full_name,
            'email': self.email,
            'department': self.department,
            'status': self.status
        }

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=1)
    department = db.Column(db.String(100))
    grade_levels = db.Column(db.String(100))  # Comma-separated grade levels
    max_students = db.Column(db.Integer, default=30)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    grades = db.relationship('Grade', backref='subject', lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='subject', lazy='dynamic')
    teachers = db.relationship('SubjectTeacher', backref='subject', lazy='dynamic')
    assignments = db.relationship('AssignmentTemplate', backref='subject', lazy='dynamic')
    
    def get_enrolled_count(self):
        """Get count of currently enrolled students"""
        return self.enrollments.filter_by(status='enrolled').count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'credits': self.credits,
            'department': self.department,
            'enrolled_count': self.get_enrolled_count(),
            'max_students': self.max_students
        }

class SubjectTeacher(db.Model):
    """Association table for Subject-Teacher relationship"""
    __tablename__ = 'subject_teacher'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    academic_year = db.Column(db.String(10))
    semester = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Grade(db.Model):
    __tablename__ = 'grade'
    __table_args__ = (
        Index('idx_grade_student', 'student_id'),
        Index('idx_grade_subject', 'subject_id'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    grade_value = db.Column(db.Float, nullable=False)  # Numeric grade (0-100)
    letter_grade = db.Column(db.String(2))  # A, B, C, D, F
    grade_type = db.Column(db.String(20))  # exam, quiz, assignment, project, midterm, final
    weight = db.Column(db.Float, default=1.0)  # Weighting for calculating final grade
    semester = db.Column(db.String(20))
    academic_year = db.Column(db.String(10))
    date_recorded = db.Column(db.Date, default=datetime.utcnow)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_letter_grade(self):
        """Convert numeric grade to letter grade"""
        if self.grade_value >= 90:
            return 'A'
        elif self.grade_value >= 80:
            return 'B'
        elif self.grade_value >= 70:
            return 'C'
        elif self.grade_value >= 60:
            return 'D'
        else:
            return 'F'
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject_id': self.subject_id,
            'grade_value': self.grade_value,
            'letter_grade': self.letter_grade,
            'grade_type': self.grade_type,
            'date_recorded': self.date_recorded.isoformat() if self.date_recorded else None
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'
    __table_args__ = (
        Index('idx_attendance_student_date', 'student_id', 'date'),
        Index('idx_attendance_date', 'date'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late, excused
    period = db.Column(db.String(20))  # morning, afternoon, or specific period
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status,
            'period': self.period,
            'notes': self.notes
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    __table_args__ = (
        Index('idx_enrollment_student', 'student_id'),
        Index('idx_enrollment_subject', 'subject_id'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(10), nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    completion_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='enrolled')  # enrolled, dropped, completed
    final_grade = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject_id': self.subject_id,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'status': self.status,
            'final_grade': self.final_grade
        }

class AssignmentTemplate(db.Model):
    """Template for assignments that can be assigned to students"""
    __tablename__ = 'assignment_template'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    assignment_type = db.Column(db.String(50))  # homework, project, essay, lab
    max_score = db.Column(db.Float, default=100.0)
    due_date = db.Column(db.DateTime)
    instructions = db.Column(db.Text)
    attachments = db.Column(db.Text)  # JSON string of file paths
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('Assignment', backref='template', lazy='dynamic')

class Assignment(db.Model):
    """Student submission for an assignment"""
    __tablename__ = 'assignment'
    __table_args__ = (
        Index('idx_assignment_student', 'student_id'),
        Index('idx_assignment_template', 'template_id'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('assignment_template.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    submission_date = db.Column(db.DateTime)
    score = db.Column(db.Float)
    status = db.Column(db.String(20), default='assigned')  # assigned, submitted, graded, late
    feedback = db.Column(db.Text)
    attachments = db.Column(db.Text)  # JSON string of submitted files
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_late(self):
        """Check if submission is late"""
        if self.template and self.template.due_date and self.submission_date:
            return self.submission_date > self.template.due_date
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'template_id': self.template_id,
            'student_id': self.student_id,
            'score': self.score,
            'status': self.status,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None
        }

class AcademicYear(db.Model):
    __tablename__ = 'academic_year'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(10), unique=True, nullable=False)  # e.g., "2023-24"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current
        }

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime)
    event_type = db.Column(db.String(50))  # exam, holiday, meeting, etc.
    location = db.Column(db.String(100))
    color = db.Column(db.String(7), default='#4f46e5')  # Hex color for calendar display
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'event_type': self.event_type,
            'location': self.location,
            'color': self.color
        }

class FeeStructure(db.Model):
    """Fee structure defining different types of fees"""
    __tablename__ = 'fee_structure'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Tuition Fee, Exam Fee, Library Fee, etc.
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)  # semester, annual, monthly, one-time
    faculty_id = db.Column(db.Integer, db.ForeignKey('subject.id'))  # Which faculty this applies to
    semester = db.Column(db.String(20))  # Which semester (1st, 2nd, etc.) - NULL for annual fees
    academic_year = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    faculty = db.relationship('Subject', backref='fee_structures')
    payments = db.relationship('FeePayment', backref='fee_structure', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'fee_type': self.fee_type,
            'faculty': self.faculty.name if self.faculty else None,
            'semester': self.semester,
            'academic_year': self.academic_year,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }

class FeePayment(db.Model):
    """Fee payments made by students"""
    __tablename__ = 'fee_payment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    fee_structure_id = db.Column(db.Integer, db.ForeignKey('fee_structure.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=date.today)
    payment_method = db.Column(db.String(50))  # cash, bank_transfer, online, card
    transaction_id = db.Column(db.String(100))  # Bank transaction reference
    receipt_number = db.Column(db.String(50), unique=True)
    remarks = db.Column(db.Text)
    payment_status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    recorded_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who recorded the payment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='fee_payments')
    recorder = db.relationship('User', backref='fee_payments_recorded')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'fee_structure_id': self.fee_structure_id,
            'amount_paid': self.amount_paid,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_method': self.payment_method,
            'receipt_number': self.receipt_number,
            'payment_status': self.payment_status
        }

class FeeReceipt(db.Model):
    """Generated receipts for fee payments"""
    __tablename__ = 'fee_receipt'
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('fee_payment.id'), nullable=False)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False)
    generated_date = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_path = db.Column(db.String(255))  # Path to generated PDF receipt
    
    # Relationships
    payment = db.relationship('FeePayment', backref='receipts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'payment_id': self.payment_id,
            'receipt_number': self.receipt_number,
            'generated_date': self.generated_date.isoformat() if self.generated_date else None
        }
