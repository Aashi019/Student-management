"""
Test database URL format for Vercel deployment
"""
import os

def test_database_url_format():
    print("🔍 Testing database URL format...")
    
    # The fixed URL without channel_binding
    NEON_DATABASE_URL = 'postgresql://neondb_owner:npg_XCrcYpHg9SO8@ep-blue-snow-ah4jpxiz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
    
    print(f"Database URL: {NEON_DATABASE_URL}")
    
    # Test SQLAlchemy URL parsing
    try:
        from sqlalchemy import create_engine
        engine = create_engine(NEON_DATABASE_URL)
        print("✅ SQLAlchemy can parse the URL format")
        
        # Test actual connection
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.fetchone()[0]
            print("✅ Database connection successful")
            print(f"PostgreSQL version: {version[:50]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_app_loading():
    print("\n🔍 Testing app loading with fixed URL...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Test that app loads without errors
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"App database URI: {db_uri}")
            
            # Quick connection test
            from models import Student
            student_count = Student.query.count()
            print(f"✅ App loads successfully, found {student_count} students")
            
        return True
        
    except Exception as e:
        print(f"❌ App loading error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Database URL Format Test")
    print("=" * 60)
    
    url_test = test_database_url_format()
    app_test = test_app_loading()
    
    if url_test and app_test:
        print("\n🎉 All tests passed! Ready for Vercel deployment.")
        print("\nDeploy with:")
        print("vercel --prod --force")
    else:
        print("\n❌ Some tests failed. Check the errors above.")