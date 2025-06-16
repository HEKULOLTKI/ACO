from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import get_db
from app.config import settings
from app.models.user import User

# OAuth2密码承载方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if current_user.status == 'inactive':
        raise HTTPException(status_code=400, detail="用户账户已被禁用")
    return current_user

def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """获取管理员用户"""
    if current_user.type != '管理员':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员权限"
        )
    return current_user

def get_operator_user(current_user: User = Depends(get_current_active_user)) -> User:
    """获取操作员用户"""
    if current_user.type not in ['管理员', '操作员']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要操作员或更高权限"
        )
    return current_user

def get_current_user_from_token(token: str, db: Session) -> User:
    """从token获取用户（用于中间件）"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        return None 