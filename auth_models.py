#!/usr/bin/env python3
"""
🔐 KMRL Authentication Models
============================
Database models and utilities for user authentication system.
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass
import bcrypt
from passlib.context import CryptContext
from jose import JWTError, jwt

# Password encryption context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@dataclass
class User:
    """User data class"""
    id: int
    username: str
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = None
    last_login: datetime = None
    role: str = "user"  # user, admin, operator

class AuthenticationManager:
    """Handles user authentication and database operations"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._create_tables()
    
    def _create_tables(self):
        """Create user tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                hashed_password TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                role TEXT DEFAULT 'user'
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Create default admin user if no users exist
        if not self.get_user_count():
            self._create_default_admin()
    
    def _create_default_admin(self):
        """Create default admin user"""
        admin_password = self.hash_password("admin123")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (username, email, full_name, hashed_password, role)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", "admin@kmrl.gov.in", "KMRL Administrator", admin_password, "admin"))
        
        conn.commit()
        conn.close()
        print("✅ Default admin user created: admin/admin123")
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return username"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
    
    def register_user(self, username: str, email: str, full_name: str, password: str, role: str = "user") -> Dict[str, Any]:
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                return {"success": False, "message": "Username or email already exists"}
            
            # Hash password and insert user
            hashed_password = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, full_name, hashed_password, role)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, full_name, hashed_password, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            return {
                "success": True, 
                "message": "User registered successfully",
                "user_id": user_id
            }
            
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        self.update_last_login(user.id)
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, full_name, hashed_password, is_active, created_at, last_login, role
            FROM users WHERE username = ?
        """, (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                full_name=row[3],
                hashed_password=row[4],
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]) if row[6] else None,
                last_login=datetime.fromisoformat(row[7]) if row[7] else None,
                role=row[8]
            )
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, full_name, hashed_password, is_active, created_at, last_login, role
            FROM users WHERE id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                full_name=row[3],
                hashed_password=row[4],
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]) if row[6] else None,
                last_login=datetime.fromisoformat(row[7]) if row[7] else None,
                role=row[8]
            )
        return None
    
    def update_last_login(self, user_id: int):
        """Update user's last login time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def create_session(self, user_id: int) -> str:
        """Create a session token for user"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, session_token, expires_at))
        
        conn.commit()
        conn.close()
        
        return session_token
    
    def verify_session(self, session_token: str) -> Optional[User]:
        """Verify session token and return user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.user_id FROM sessions s
            WHERE s.session_token = ? AND s.expires_at > CURRENT_TIMESTAMP
        """, (session_token,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self.get_user_by_id(row[0])
        return None
    
    def logout_user(self, session_token: str):
        """Logout user by removing session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_token = ?", (session_token,))
        
        conn.commit()
        conn.close()
    
    def get_all_users(self) -> list[User]:
        """Get all users (for admin)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, full_name, hashed_password, is_active, created_at, last_login, role
            FROM users ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        users = []
        for row in rows:
            users.append(User(
                id=row[0],
                username=row[1],
                email=row[2],
                full_name=row[3],
                hashed_password=row[4],
                is_active=bool(row[5]),
                created_at=datetime.fromisoformat(row[6]) if row[6] else None,
                last_login=datetime.fromisoformat(row[7]) if row[7] else None,
                role=row[8]
            ))
        
        return users

# Global auth manager instance
auth_manager = AuthenticationManager()