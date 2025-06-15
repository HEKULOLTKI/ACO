from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    """任务基础模式"""
    name: str
    type: Optional[str] = None
    phase: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = '未分配'

class TaskCreate(TaskBase):
    """创建任务模式"""
    pass

class TaskUpdate(BaseModel):
    """更新任务模式"""
    name: Optional[str] = None
    type: Optional[str] = None
    phase: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Task(TaskBase):
    """任务响应模式"""
    id: int
    create_time: datetime
    update_time: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TaskInDB(Task):
    """数据库中的任务模式"""
    pass

# 批量导入结果
class TaskBulkImportResult(BaseModel):
    """任务批量导入结果"""
    success_count: int
    fail_count: int
    failed_tasks: List[dict]
    message: str

class TaskAssignmentBase(BaseModel):
    """任务分配基础模式"""
    task_id: int
    user_id: Optional[int] = None
    username: str
    status: Optional[str] = '进行中'
    progress: Optional[int] = 0
    performance_score: Optional[int] = 0
    comments: Optional[str] = None

class TaskAssignmentCreate(TaskAssignmentBase):
    """任务分配创建模式"""
    pass

class TaskAssignmentUpdate(BaseModel):
    """任务分配更新模式"""
    status: Optional[str] = None
    progress: Optional[int] = None
    performance_score: Optional[int] = None
    comments: Optional[str] = None

class TaskAssignmentResponse(TaskAssignmentBase):
    """任务分配响应模式"""
    id: int
    assigned_at: datetime
    last_update: datetime
    # 任务信息
    task_name: Optional[str] = None
    task_type: Optional[str] = None
    task_phase: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class TaskWithAssignments(Task):
    """包含分配信息的任务模式"""
    assignments: List[TaskAssignmentResponse] = [] 