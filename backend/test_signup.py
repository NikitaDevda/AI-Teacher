import sys
sys.path.append('.')

from database import init_db, SessionLocal
from services.auth_service import auth_service

# Initialize database
init_db()

# Create test user
db = SessionLocal()

try:
    print("🧪 Testing user creation...")
    
    user, token = auth_service.create_user(
        db=db,
        email="test@example.com",
        username="testuser",
        password="password123",
        full_name="Test User"
    )
    
    print(f"✅ User created successfully!")
    print(f"   ID: {user.id}")
    print(f"   Email: {user.email}")
    print(f"   Username: {user.username}")
    print(f"   Verified: {user.is_verified}")
    
except Exception as e:
    print(f"❌ Error: {e}")

finally:
    db.close()