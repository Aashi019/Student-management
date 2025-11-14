"""
Quick deployment verification script
Run this before deploying to ensure everything is configured correctly
"""

import os
import sys

def check_configuration():
    print("🔍 Checking deployment configuration...")
    
    # Check 1: Database configuration
    try:
        from app import app, db
        with app.app_context():
            # Check database URI
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'postgresql' in db_uri and 'neondb' in db_uri:
                print("✅ Database: PostgreSQL configured correctly")
            else:
                print(f"❌ Database: Incorrect configuration - {db_uri}")
                return False
            
            # Test connection
            with db.engine.connect() as connection:
                result = connection.execute(db.text('SELECT 1'))
                print("✅ Database: Connection test successful")
                
    except Exception as e:
        print(f"❌ Database: Connection failed - {e}")
        return False
    
    # Check 2: Vercel configuration
    vercel_config_exists = os.path.exists('vercel.json')
    if vercel_config_exists:
        print("✅ Vercel: vercel.json exists")
    else:
        print("❌ Vercel: vercel.json missing")
        return False
    
    # Check 3: Requirements
    requirements_exists = os.path.exists('requirements.txt')
    if requirements_exists:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            if 'psycopg2-binary' in content:
                print("✅ Dependencies: PostgreSQL driver included")
            else:
                print("❌ Dependencies: PostgreSQL driver missing")
                return False
    else:
        print("❌ Dependencies: requirements.txt missing")
        return False
    
    # Check 4: No SQLite files
    sqlite_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.db'):
                sqlite_files.append(os.path.join(root, file))
    
    if not sqlite_files:
        print("✅ Cleanup: No SQLite files found")
    else:
        print(f"⚠️  Cleanup: SQLite files found: {sqlite_files}")
    
    print("\n🎉 All checks passed! Ready for deployment.")
    return True

if __name__ == '__main__':
    success = check_configuration()
    
    if success:
        print("\n📝 Deploy with:")
        print("vercel --prod")
        print("\nOr force redeploy:")
        print("vercel --prod --force")
    else:
        print("\n❌ Fix the issues above before deploying")
        sys.exit(1)