from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session 
from database import User, UserProfile
import secrets
import os 

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        plain_password = plain_password[:72]
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password"""
        password = password[:72]
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def create_user(db: Session, email: str, username: str, password: str, full_name: str = None):
        """Create new user"""
        
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing_user:
            if existing_user.email == email:
                raise ValueError("Email already registered")
            else:
                raise ValueError("Username already taken")
        
        # Create user
        hashed_password = AuthService.get_password_hash(password)
        verification_token = secrets.token_urlsafe(32)
        
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            verification_token=verification_token,
            is_verified=True  # Auto-verify for development
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create profile
        profile = UserProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        
        print(f"✅ User created: {username} ({email})")
        
        return user, verification_token
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """Authenticate user"""
        
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ User not found: {email}")
            return None
        
        if not AuthService.verify_password(password, user.hashed_password):
            print(f"❌ Invalid password for: {email}")
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        print(f"✅ User authenticated: {user.username}")
        return user
    
    @staticmethod
    def verify_email(db: Session, token: str):
        """Verify email with token"""
        
        user = db.query(User).filter(User.verification_token == token).first()
        
        if not user:
            return False
        
        user.is_verified = True
        user.verification_token = None
        db.commit()
        
        return True
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()


auth_service = AuthService()
