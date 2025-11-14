"""
Simple test to verify PostgreSQL database connection
"""
import os
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_XCrcYpHg9SO8@ep-blue-snow-ah4jpxiz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

from app import app
from models import User, Student, Subject

with app.app_context():
    users = User.query.count()
    students = Student.query.count()
    subjects = Subject.query.count()
    
    print(f"SUCCESS: Application loads with PostgreSQL!")
    print(f"Users: {users}")
    print(f"Students: {students}")
    print(f"Subjects: {subjects}")
    
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print(f"Admin user found: {admin.username}")
    
    print("PostgreSQL database integration successful!")