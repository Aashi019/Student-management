from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField, SelectField, DateField, FloatField, BooleanField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional(), Length(max=50)])
    state = StringField('State', validators=[Optional(), Length(max=50)])
    zip_code = StringField('ZIP Code', validators=[Optional(), Length(max=10)])
    emergency_contact = StringField('Emergency Contact Name', validators=[Optional(), Length(max=100)])
    emergency_phone = StringField('Emergency Contact Phone', validators=[Optional(), Length(max=20)])
    grade_level = SelectField('Year Level', choices=[
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year')
    ], validators=[DataRequired()])
    graduation_year = IntegerField('Expected Graduation Year', validators=[
        Optional(),
        NumberRange(min=datetime.now().year, max=datetime.now().year + 20)
    ])
    photo = FileField('Student Photo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Save Student')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Subject Code', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Optional()])
    credits = IntegerField('Credits', validators=[DataRequired(), NumberRange(min=1, max=10)])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Save Subject')

class GradeForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    grade_value = FloatField('Grade (0-100)', validators=[
        DataRequired(),
        NumberRange(min=0, max=100)
    ])
    letter_grade = SelectField('Letter Grade', choices=[
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D+', 'D+'),
        ('D', 'D'),
        ('F', 'F')
    ], validators=[DataRequired()])
    grade_type = SelectField('Grade Type', choices=[
        ('exam', 'Exam'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('participation', 'Participation'),
        ('final', 'Final Grade')
    ], validators=[DataRequired()])
    semester = SelectField('Semester', choices=[
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer')
    ], validators=[DataRequired()])
    academic_year = StringField('Academic Year (e.g., 2024-25)', validators=[DataRequired()])
    date_recorded = DateField('Date Recorded', default=datetime.today, validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[Optional()])
    submit = SubmitField('Save Grade')

class AttendanceForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    date = DateField('Date', default=datetime.today, validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused Absence')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Attendance')

class BulkAttendanceForm(FlaskForm):
    date = DateField('Date', default=datetime.today, validators=[DataRequired()])
    submit = SubmitField('Load Students')

class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    semester = SelectField('Semester', choices=[
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer')
    ], validators=[DataRequired()])
    academic_year = StringField('Academic Year (e.g., 2024-25)', validators=[DataRequired()])
    submit = SubmitField('Enroll Student')

class SearchForm(FlaskForm):
    search = StringField('Search students...', validators=[Optional()])
    grade_filter = SelectField('Grade Level', choices=[('', 'All Grades')], validators=[Optional()])
    status_filter = SelectField('Status', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('transferred', 'Transferred')
    ], default='active', validators=[Optional()])
    submit = SubmitField('Search')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff')
    ], validators=[DataRequired()])
    submit = SubmitField('Save User')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')
