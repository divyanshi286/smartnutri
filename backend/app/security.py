import bcrypt
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

# Setup encryption key - if not set or is a placeholder, generate a new one
_encryption_key = os.getenv("ENCRYPTION_KEY", "").strip()
if _encryption_key and not _encryption_key.startswith("your-"):
    ENCRYPTION_KEY = _encryption_key.encode() if isinstance(_encryption_key, str) else _encryption_key
else:
    ENCRYPTION_KEY = Fernet.generate_key()

cipher_suite = Fernet(ENCRYPTION_KEY)

# Password hashing
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hash_value: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hash_value.encode())

# JWT tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, remember_me: bool = False) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # 7 days standard expiry for health data security
        expire = datetime.utcnow() + timedelta(days=7)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Encryption for sensitive data
def encrypt_data(data: str) -> str:
    """Encrypt data using Fernet (AES-256)"""
    if isinstance(data, str):
        data = data.encode()
    encrypted = cipher_suite.encrypt(data)
    return encrypted.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt Fernet-encrypted data"""
    try:
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        decrypted = cipher_suite.decrypt(encrypted_data)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None
