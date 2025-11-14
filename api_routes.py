"""
RESTful API Routes for School Management System
Provides comprehensive CRUD operations for all entities
"""

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from models import db, Student, Teacher, Subject, Grade, Attendance, Enrollment, Assignment, AssignmentTemplate, Event, AcademicYear, SubjectTeacher
from datetime import datetime, date, timedelta
from sqlalchemy import func, desc, or_
from werkzeug.utils import secure_filename
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Store socketio instance (will be set from app.py)
socketio_instance = None

def set_socketio(socketio):
    """Set the socketio instance from app.py"""
    global socketio_instance
    socketio_instance = socketio

# Helper to emit socket events
def emit_socket_event(event_name, data):
    """Emit a socket.io event if socketio is available"""
    if socketio_instance:
        try:
            socketio_instance.emit(event_name, data, broadcast=True, namespace='/')
        except Exception as e:
            print(f"Socket emit error: {e}")
            pass

# ==================== HELPER FUNCTIONS ====================

def success_response(data=None, message="Success", status=200):
    """Standard success response format"""
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status

def error_response(message="Error", status=400, errors=None):
    """Standard error response format"""
    response = {
        'success': False,
        'message': message,
        'errors': errors or []
    }
    return jsonify(response), status

def parse_date(date_string):
    """Parse date string to date object"""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None

# ==================== STUDENT API ====================

@api_bp.route('/students', methods=['GET'])
@login_required
def get_students():
    """Get all students with filters and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    grade_filter = request.args.get('grade', '')
    status_filter = request.args.get('status', 'active')
    
    query = Student.query
    
    if search:
        query = query.filter(
            or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.email.ilike(f'%{search}%'),
                Student.student_id.ilike(f'%{search}%')
            )
        )
    
    if grade_filter:
        query = query.filter(Student.grade_level == grade_filter)
    
    if status_filter:
        query = query.filter(Student.status == status_filter)
    
    pagination = query.order_by(Student.last_name, Student.first_name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    students = [student.to_dict() for student in pagination.items]
    
    return success_response({
        'students': students,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@api_bp.route('/students/<int:id>', methods=['GET'])
@login_required
def get_student(id):
    """Get a single student by ID"""
    student = Student.query.get_or_404(id)
    
    # Get additional data
    grades = [g.to_dict() for g in student.grades.limit(10).all()]
    attendance_rate = student.get_attendance_rate()
    
    return success_response({
        'student': student.to_dict(),
        'grades': grades,
        'attendance_rate': attendance_rate
    })

@api_bp.route('/students', methods=['POST'])
@login_required
def create_student():
    """Create a new student"""
    data = request.get_json()
    
    try:
        # Generate unique student ID
        last_student = Student.query.order_by(desc(Student.id)).first()
        next_id = (last_student.id + 1) if last_student else 1
        student_id = f"STU{next_id:06d}"
        
        student = Student(
            student_id=student_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            date_of_birth=parse_date(data.get('date_of_birth')),
            gender=data.get('gender'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            zip_code=data.get('zip_code'),
            emergency_contact=data.get('emergency_contact'),
            emergency_phone=data.get('emergency_phone'),
            parent_email=data.get('parent_email'),
            grade_level=data.get('grade_level'),
            graduation_year=data.get('graduation_year'),
            medical_info=data.get('medical_info'),
            notes=data.get('notes')
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Emit real-time update
        emit_socket_event('student_created', student.to_dict())
        
        return success_response(student.to_dict(), "Student created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating student: {str(e)}", 400)

@api_bp.route('/students/<int:id>', methods=['PUT'])
@login_required
def update_student(id):
    """Update an existing student"""
    student = Student.query.get_or_404(id)
    data = request.get_json()
    
    try:
        # Update fields
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.phone = data.get('phone', student.phone)
        student.gender = data.get('gender', student.gender)
        student.address = data.get('address', student.address)
        student.city = data.get('city', student.city)
        student.state = data.get('state', student.state)
        student.zip_code = data.get('zip_code', student.zip_code)
        student.emergency_contact = data.get('emergency_contact', student.emergency_contact)
        student.emergency_phone = data.get('emergency_phone', student.emergency_phone)
        student.parent_email = data.get('parent_email', student.parent_email)
        student.grade_level = data.get('grade_level', student.grade_level)
        student.graduation_year = data.get('graduation_year', student.graduation_year)
        student.status = data.get('status', student.status)
        student.medical_info = data.get('medical_info', student.medical_info)
        student.notes = data.get('notes', student.notes)
        
        if data.get('date_of_birth'):
            student.date_of_birth = parse_date(data.get('date_of_birth'))
        
        student.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(student.to_dict(), "Student updated successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating student: {str(e)}", 400)

@api_bp.route('/students/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    """Soft delete a student (set status to inactive)"""
    student = Student.query.get_or_404(id)
    
    try:
        student.status = 'inactive'
        student.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(None, "Student deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting student: {str(e)}", 400)

# ==================== SUBJECT API ====================

@api_bp.route('/subjects', methods=['GET'])
@login_required
def get_subjects():
    """Get all subjects"""
    subjects = Subject.query.filter_by(is_active=True).all()
    return success_response([subject.to_dict() for subject in subjects])

@api_bp.route('/subjects/<int:id>', methods=['GET'])
@login_required
def get_subject(id):
    """Get a single subject"""
    subject = Subject.query.get_or_404(id)
    
    # Get enrolled students
    enrollments = subject.enrollments.filter_by(status='enrolled').all()
    students = [{'id': e.student.id, 'name': e.student.full_name} for e in enrollments]
    
    return success_response({
        'subject': subject.to_dict(),
        'enrolled_students': students
    })

@api_bp.route('/subjects', methods=['POST'])
@login_required
def create_subject():
    """Create a new subject"""
    data = request.get_json()
    
    try:
        subject = Subject(
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description'),
            credits=data.get('credits', 1),
            department=data.get('department'),
            grade_levels=data.get('grade_levels'),
            max_students=data.get('max_students', 30)
        )
        
        db.session.add(subject)
        db.session.commit()
        
        return success_response(subject.to_dict(), "Subject created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating subject: {str(e)}", 400)

@api_bp.route('/subjects/<int:id>', methods=['PUT'])
@login_required
def update_subject(id):
    """Update an existing subject"""
    subject = Subject.query.get_or_404(id)
    data = request.get_json()
    
    try:
        subject.name = data.get('name', subject.name)
        subject.code = data.get('code', subject.code)
        subject.description = data.get('description', subject.description)
        subject.credits = data.get('credits', subject.credits)
        subject.department = data.get('department', subject.department)
        subject.grade_levels = data.get('grade_levels', subject.grade_levels)
        subject.max_students = data.get('max_students', subject.max_students)
        subject.is_active = data.get('is_active', subject.is_active)
        subject.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(subject.to_dict(), "Subject updated successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating subject: {str(e)}", 400)

@api_bp.route('/subjects/<int:id>', methods=['DELETE'])
@login_required
def delete_subject(id):
    """Soft delete a subject"""
    subject = Subject.query.get_or_404(id)
    
    try:
        subject.is_active = False
        subject.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(None, "Subject deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting subject: {str(e)}", 400)

# ==================== ATTENDANCE API ====================

@api_bp.route('/attendance', methods=['GET'])
@login_required
def get_attendance():
    """Get attendance records with filters"""
    date_str = request.args.get('date')
    student_id = request.args.get('student_id', type=int)
    status = request.args.get('status')
    
    query = Attendance.query
    
    if date_str:
        query = query.filter(Attendance.date == parse_date(date_str))
    
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    
    if status:
        query = query.filter(Attendance.status == status)
    
    records = query.order_by(desc(Attendance.date)).limit(100).all()
    
    return success_response([record.to_dict() for record in records])

@api_bp.route('/attendance', methods=['POST'])
@login_required
def create_attendance():
    """Create a new attendance record"""
    data = request.get_json()
    
    try:
        attendance = Attendance(
            student_id=data.get('student_id'),
            date=parse_date(data.get('date')),
            status=data.get('status'),
            period=data.get('period'),
            notes=data.get('notes'),
            recorded_by=current_user.id
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return success_response(attendance.to_dict(), "Attendance recorded successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating attendance: {str(e)}", 400)

@api_bp.route('/attendance/bulk', methods=['POST'])
@login_required
def bulk_attendance():
    """Create multiple attendance records at once"""
    data = request.get_json()
    records = data.get('records', [])
    
    try:
        for record in records:
            attendance = Attendance(
                student_id=record.get('student_id'),
                date=parse_date(record.get('date')),
                status=record.get('status'),
                period=record.get('period'),
                recorded_by=current_user.id
            )
            db.session.add(attendance)
        
        db.session.commit()
        
        return success_response(None, f"{len(records)} attendance records created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating bulk attendance: {str(e)}", 400)

@api_bp.route('/attendance/<int:id>', methods=['PUT'])
@login_required
def update_attendance(id):
    """Update an attendance record"""
    attendance = Attendance.query.get_or_404(id)
    data = request.get_json()
    
    try:
        attendance.status = data.get('status', attendance.status)
        attendance.period = data.get('period', attendance.period)
        attendance.notes = data.get('notes', attendance.notes)
        attendance.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(attendance.to_dict(), "Attendance updated successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating attendance: {str(e)}", 400)

@api_bp.route('/attendance/<int:id>', methods=['DELETE'])
@login_required
def delete_attendance(id):
    """Delete an attendance record"""
    attendance = Attendance.query.get_or_404(id)
    
    try:
        db.session.delete(attendance)
        db.session.commit()
        
        return success_response(None, "Attendance deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting attendance: {str(e)}", 400)

# ==================== GRADE API ====================

@api_bp.route('/grades', methods=['GET'])
@login_required
def get_grades():
    """Get grades with filters"""
    student_id = request.args.get('student_id', type=int)
    subject_id = request.args.get('subject_id', type=int)
    
    query = Grade.query
    
    if student_id:
        query = query.filter(Grade.student_id == student_id)
    
    if subject_id:
        query = query.filter(Grade.subject_id == subject_id)
    
    grades = query.order_by(desc(Grade.date_recorded)).limit(100).all()
    
    return success_response([grade.to_dict() for grade in grades])

@api_bp.route('/grades', methods=['POST'])
@login_required
def create_grade():
    """Create a new grade"""
    data = request.get_json()
    
    try:
        grade = Grade(
            student_id=data.get('student_id'),
            subject_id=data.get('subject_id'),
            grade_value=data.get('grade_value'),
            grade_type=data.get('grade_type'),
            weight=data.get('weight', 1.0),
            semester=data.get('semester'),
            academic_year=data.get('academic_year'),
            comments=data.get('comments')
        )
        
        # Auto-calculate letter grade
        grade.letter_grade = grade.calculate_letter_grade()
        
        db.session.add(grade)
        db.session.commit()
        
        # Update student GPA
        student = Student.query.get(grade.student_id)
        if student:
            student.gpa = student.calculate_gpa()
            db.session.commit()
        
        return success_response(grade.to_dict(), "Grade created successfully", 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating grade: {str(e)}", 400)

@api_bp.route('/grades/<int:id>', methods=['PUT'])
@login_required
def update_grade(id):
    """Update a grade"""
    grade = Grade.query.get_or_404(id)
    data = request.get_json()
    
    try:
        grade.grade_value = data.get('grade_value', grade.grade_value)
        grade.grade_type = data.get('grade_type', grade.grade_type)
        grade.weight = data.get('weight', grade.weight)
        grade.comments = data.get('comments', grade.comments)
        grade.letter_grade = grade.calculate_letter_grade()
        grade.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Update student GPA
        student = Student.query.get(grade.student_id)
        if student:
            student.gpa = student.calculate_gpa()
            db.session.commit()
        
        return success_response(grade.to_dict(), "Grade updated successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating grade: {str(e)}", 400)

@api_bp.route('/grades/<int:id>', methods=['DELETE'])
@login_required
def delete_grade(id):
    """Delete a grade"""
    grade = Grade.query.get_or_404(id)
    student_id = grade.student_id
    
    try:
        db.session.delete(grade)
        db.session.commit()
        
        # Update student GPA
        student = Student.query.get(student_id)
        if student:
            student.gpa = student.calculate_gpa()
            db.session.commit()
        
        return success_response(None, "Grade deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting grade: {str(e)}", 400)

# ==================== STATISTICS API ====================

@api_bp.route('/stats/dashboard', methods=['GET'])
@login_required
def get_dashboard_stats():
    """Get comprehensive dashboard statistics"""
    
    # Student statistics
    total_students = Student.query.filter_by(status='active').count()
    total_subjects = Subject.query.filter_by(is_active=True).count()
    
    # Recent enrollments (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_enrollments = Student.query.filter(
        Student.enrollment_date >= thirty_days_ago.date()
    ).count()
    
    # Attendance rate (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    total_attendance = Attendance.query.filter(
        func.extract('month', Attendance.date) == current_month,
        func.extract('year', Attendance.date) == current_year
    ).count()
    
    present_attendance = Attendance.query.filter(
        func.extract('month', Attendance.date) == current_month,
        func.extract('year', Attendance.date) == current_year,
        Attendance.status == 'present'
    ).count()
    
    attendance_rate = round((present_attendance / total_attendance * 100), 1) if total_attendance > 0 else 0
    
    # Average GPA
    avg_gpa = db.session.query(func.avg(Student.gpa)).scalar() or 0
    avg_gpa = round(avg_gpa, 2)
    
    # Grade distribution
    grade_dist = db.session.query(
        Grade.letter_grade,
        func.count(Grade.id).label('count')
    ).group_by(Grade.letter_grade).all()
    
    grade_distribution = [{'grade': g[0], 'count': g[1]} for g in grade_dist if g[0]]
    
    # Students by grade level
    grade_level_dist = db.session.query(
        Student.grade_level,
        func.count(Student.id).label('count')
    ).filter(Student.status == 'active').group_by(Student.grade_level).all()
    
    students_by_grade = [{'grade': g[0], 'count': g[1]} for g in grade_level_dist]
    
    # Enrollment trend (last 12 months)
    enrollment_trend = []
    for i in range(12):
        date = datetime.now() - timedelta(days=30*i)
        count = Student.query.filter(
            Student.enrollment_date <= date.date()
        ).count()
        enrollment_trend.append({
            'month': date.strftime('%b %Y'),
            'count': count
        })
    
    return success_response({
        'overview': {
            'total_students': total_students,
            'total_subjects': total_subjects,
            'recent_enrollments': recent_enrollments,
            'attendance_rate': attendance_rate,
            'average_gpa': avg_gpa
        },
        'grade_distribution': grade_distribution,
        'students_by_grade': students_by_grade,
        'enrollment_trend': list(reversed(enrollment_trend))
    })

@api_bp.route('/stats/attendance-trend', methods=['GET'])
@login_required
def get_attendance_trend():
    """Get attendance trend for last 30 days"""
    days = request.args.get('days', 30, type=int)
    
    trend = []
    for i in range(days):
        date = datetime.now().date() - timedelta(days=i)
        total = Attendance.query.filter(Attendance.date == date).count()
        present = Attendance.query.filter(
            Attendance.date == date,
            Attendance.status == 'present'
        ).count()
        
        rate = round((present / total * 100), 1) if total > 0 else 0
        trend.append({
            'date': date.isoformat(),
            'rate': rate,
            'total': total,
            'present': present
        })
    
    return success_response(list(reversed(trend)))
