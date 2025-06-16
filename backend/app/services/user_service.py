from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, BulkImportResult
from app.utils.security import get_password_hash, verify_password
import logging

# 设置日志
logger = logging.getLogger(__name__)

class UserService:
    """用户服务类"""
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """获取用户列表"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """创建用户"""
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            password=hashed_password,
            role=user.role,
            type=user.type,
            status=user.status
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """删除用户"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    def get_users_by_role(db: Session, role: str) -> List[User]:
        """根据角色获取用户"""
        return db.query(User).filter(User.role == role).all()
    
    @staticmethod
    def get_users_by_type(db: Session, user_type: str) -> List[User]:
        """根据类型获取用户"""
        return db.query(User).filter(User.type == user_type).all()
    
    @staticmethod
    def update_user_status(db: Session, user_id: int, status: str) -> Optional[User]:
        """更新用户状态"""
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.status = status
            db.commit()
            db.refresh(db_user)
        return db_user
    
    @staticmethod
    def bulk_create_users(db: Session, users: List[UserCreate]) -> BulkImportResult:
        """批量创建用户"""
        success_count = 0
        fail_count = 0
        failed_users = []
        
        for user_data in users:
            try:
                # 检查用户名是否已存在
                existing_user = UserService.get_user_by_username(db, user_data.username)
                if existing_user:
                    fail_count += 1
                    failed_users.append({
                        "username": user_data.username,
                        "error": "用户名已存在"
                    })
                    continue
                
                # 创建用户
                hashed_password = get_password_hash(user_data.password)
                db_user = User(
                    username=user_data.username,
                    password=hashed_password,
                    role=user_data.role,
                    type=user_data.type,
                    status=user_data.status or 'inactive'
                )
                db.add(db_user)
                success_count += 1
                
            except Exception as e:
                logger.error(f"创建用户 {user_data.username} 失败: {str(e)}")
                fail_count += 1
                failed_users.append({
                    "username": user_data.username,
                    "error": str(e)
                })
        
        try:
            db.commit()
        except Exception as e:
            logger.error(f"批量创建用户事务提交失败: {str(e)}")
            db.rollback()
            return BulkImportResult(
                success_count=0,
                fail_count=len(users),
                failed_users=[{"username": user.username, "error": "数据库操作失败"} for user in users],
                message="批量导入失败"
            )
        
        message = f"批量导入完成：成功 {success_count} 个，失败 {fail_count} 个"
        return BulkImportResult(
            success_count=success_count,
            fail_count=fail_count,
            failed_users=failed_users,
            message=message
        ) 