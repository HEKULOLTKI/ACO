from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
import warnings

# 忽略passlib的bcrypt版本警告
warnings.filterwarnings("ignore", message=".*__about__.*")

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # 如果出现版本兼容性问题，记录但不抛出异常
        print(f"Password verification warning: {e}")
        # 尝试再次验证
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except:
            return False

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing warning: {e}")
        # 尝试再次生成
        return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """验证令牌并返回用户名"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None 