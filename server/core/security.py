from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
import hashlib
import base64
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _preprocess_password(password: str) -> str:
    """
    Preprocess password to ensure it never exceeds bcrypt's 72-byte limit.
    Uses SHA-256 to hash long passwords, then base64 encodes for consistent length.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Hash with SHA-256 and encode to base64 for passwords exceeding 72 bytes
        hashed = hashlib.sha256(password_bytes).digest()
        return base64.b64encode(hashed).decode('ascii')
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    processed_password = _preprocess_password(plain_password)
    return pwd_context.verify(processed_password, hashed_password)

def get_password_hash(password: str) -> str:
    processed_password = _preprocess_password(password)
    return pwd_context.hash(processed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt