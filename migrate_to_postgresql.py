"""
Database Migration Script for PostgreSQL (Neon)
This script initializes the PostgreSQL database with tables and sample data.
"""

import os
import sys
from datetime import datetime

# Set up the database URL if not already set
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_XCrcYpHg9SO8@ep-blue-snow-ah4jpxiz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

try:
    from app import app, db
    from models import *
    import create_sample_data
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you've installed all dependencies: pip install -r requirements.txt")
    sys.exit(1)

def init_postgresql_database():
    """Initialize PostgreSQL database with tables and sample data"""
    print("🚀 Starting PostgreSQL database initialization...")
    
    with app.app_context():
        try:
            # Test database connection
            print("📊 Testing database connection...")
            with db.engine.connect() as connection:
                result = connection.execute(db.text('SELECT 1'))
                print("✅ Database connection successful!")
            
            # Drop all tables (for clean setup)
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("🏗️  Creating database tables...")
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Create sample data
            print("📝 Creating sample data...")
            create_sample_data.create_sample_data()
            print("✅ Sample data created successfully!")
            
            # Verify data was created
            print("🔍 Verifying data creation...")
            user_count = User.query.count()
            student_count = Student.query.count()
            subject_count = Subject.query.count()
            
            print(f"📊 Database initialized with:")
            print(f"   - {user_count} users")
            print(f"   - {student_count} students") 
            print(f"   - {subject_count} subjects")
            
            print("🎉 PostgreSQL database initialization completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during database initialization: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False

def test_database_operations():
    """Test basic database operations"""
    print("\n🧪 Testing database operations...")
    
    with app.app_context():
        try:
            # Test query
            students = Student.query.limit(5).all()
            print(f"✅ Successfully queried {len(students)} students")
            
            # Test specific operations
            admin_user = User.query.filter_by(role='admin').first()
            if admin_user:
                print(f"✅ Found admin user: {admin_user.username}")
            
            active_students = Student.query.filter_by(status='active').count()
            print(f"✅ Found {active_students} active students")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing database operations: {e}")
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("🐘 PostgreSQL Database Migration Script")
    print("=" * 60)
    
    # Initialize database
    success = init_postgresql_database()
    
    if success:
        # Test operations
        test_success = test_database_operations()
        
        if test_success:
            print("\n🎉 All tests passed! Your PostgreSQL database is ready to use.")
            print("\n📝 Next steps:")
            print("   1. Install PostgreSQL dependencies: pip install -r requirements.txt")
            print("   2. Run your application: python app.py")
            print("   3. Deploy to Vercel with DATABASE_URL environment variable")
        else:
            print("\n⚠️  Database initialized but some tests failed. Check the errors above.")
    else:
        print("\n❌ Database initialization failed. Please check the errors above.")
        sys.exit(1)