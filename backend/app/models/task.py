from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="任务名称")
    type = Column(String(100), comment="任务类型")
    phase = Column(String(50), comment="任务阶段")
    description = Column(Text, comment="任务描述")
    status = Column(String(50), default='未分配', comment="任务状态")
    role_binding = Column(String(100), comment="绑定角色")
    create_time = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    update_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    assignments = relationship("TaskAssignment", back_populates="task")
    
    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}', status='{self.status}')>"

class TaskAssignment(Base):
    """任务分配模型"""
    __tablename__ = "task_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), comment="任务ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    username = Column(String(255), comment="用户名")
    assigned_at = Column(TIMESTAMP, server_default=func.now(), comment="分配时间")
    status = Column(String(50), default='进行中', comment="执行状态")
    progress = Column(Integer, default=0, comment="进度百分比")
    performance_score = Column(Integer, default=0, comment="性能评分")
    comments = Column(Text, comment="备注")
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="最后更新")
    
    # 关联关系
    task = relationship("Task", back_populates="assignments")
    user = relationship("User", back_populates="task_assignments")
    
    def __repr__(self):
        return f"<TaskAssignment(id={self.id}, task_id={self.task_id}, username='{self.username}')>" 