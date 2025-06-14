from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.task import Task, TaskAssignment
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskAssignmentCreate, TaskAssignmentUpdate

class TaskService:
    """任务服务类"""
    
    @staticmethod
    def get_task(db: Session, task_id: int) -> Optional[Task]:
        """根据ID获取任务"""
        return db.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 100, 
                  status: Optional[str] = None, task_type: Optional[str] = None) -> List[Task]:
        """获取任务列表，支持状态和类型过滤"""
        query = db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if task_type:
            query = query.filter(Task.type == task_type)
            
        return query.order_by(desc(Task.create_time)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_tasks_count(db: Session, status: Optional[str] = None, 
                       task_type: Optional[str] = None) -> int:
        """获取任务总数"""
        query = db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if task_type:
            query = query.filter(Task.type == task_type)
            
        return query.count()
    
    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:
        """创建任务"""
        db_task = Task(
            name=task.name,
            type=task.type,
            phase=task.phase,
            description=task.description,
            status=task.status or '未分配'
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
        """更新任务"""
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
            
        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
            
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """删除任务"""
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return False
            
        # 先删除相关的任务分配
        db.query(TaskAssignment).filter(TaskAssignment.task_id == task_id).delete()
        db.delete(db_task)
        db.commit()
        return True
    
    @staticmethod
    def get_task_with_assignments(db: Session, task_id: int) -> Optional[Task]:
        """获取包含分配信息的任务"""
        return db.query(Task).filter(Task.id == task_id).first()

class TaskAssignmentService:
    """任务分配服务类"""
    
    @staticmethod
    def get_assignment(db: Session, assignment_id: int) -> Optional[TaskAssignment]:
        """根据ID获取任务分配"""
        return db.query(TaskAssignment).filter(TaskAssignment.id == assignment_id).first()
    
    @staticmethod
    def get_assignments_by_task(db: Session, task_id: int) -> List[TaskAssignment]:
        """根据任务ID获取分配列表"""
        return db.query(TaskAssignment).filter(TaskAssignment.task_id == task_id).all()
    
    @staticmethod
    def get_assignments_by_user(db: Session, user_id: int, 
                               status: Optional[str] = None) -> List[TaskAssignment]:
        """根据用户ID获取分配列表"""
        query = db.query(TaskAssignment).filter(TaskAssignment.user_id == user_id)
        
        if status:
            query = query.filter(TaskAssignment.status == status)
            
        assignments = query.order_by(desc(TaskAssignment.assigned_at)).all()
        
        # 填充任务信息
        for assignment in assignments:
            task = db.query(Task).filter(Task.id == assignment.task_id).first()
            if task:
                assignment.task_name = task.name
                assignment.task_type = task.type
                assignment.task_phase = task.phase
        
        return assignments
    
    @staticmethod
    def get_assignments(db: Session, skip: int = 0, limit: int = 100,
                       status: Optional[str] = None) -> List[TaskAssignment]:
        """获取任务分配列表"""
        query = db.query(TaskAssignment)
        
        if status:
            query = query.filter(TaskAssignment.status == status)
            
        assignments = query.order_by(desc(TaskAssignment.assigned_at)).offset(skip).limit(limit).all()
        
        # 填充任务信息
        for assignment in assignments:
            task = db.query(Task).filter(Task.id == assignment.task_id).first()
            if task:
                assignment.task_name = task.name
                assignment.task_type = task.type
                assignment.task_phase = task.phase
        
        return assignments
    
    @staticmethod
    def create_assignment(db: Session, assignment: TaskAssignmentCreate) -> Optional[TaskAssignment]:
        """创建任务分配"""
        # 检查任务是否存在
        task = db.query(Task).filter(Task.id == assignment.task_id).first()
        if not task:
            return None
            
        # 检查用户是否存在
        user = None
        if assignment.user_id:
            user = db.query(User).filter(User.id == assignment.user_id).first()
            if not user:
                return None
        elif assignment.username:
            # 如果没有user_id但有username，尝试通过username查找用户
            user = db.query(User).filter(User.username == assignment.username).first()
            if user:
                assignment.user_id = user.id
        
        # 创建分配
        db_assignment = TaskAssignment(
            task_id=assignment.task_id,
            user_id=assignment.user_id,
            username=assignment.username,
            status=assignment.status or '进行中',
            progress=assignment.progress or 0,
            performance_score=assignment.performance_score or 0,
            comments=assignment.comments
        )
        
        # 更新任务状态
        if task.status == '未分配':
            task.status = '进行中'
            
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        
        # 填充任务信息
        if task:
            db_assignment.task_name = task.name
            db_assignment.task_type = task.type
            db_assignment.task_phase = task.phase
        
        return db_assignment
    
    @staticmethod
    def update_assignment(db: Session, assignment_id: int, 
                         assignment: TaskAssignmentUpdate) -> Optional[TaskAssignment]:
        """更新任务分配"""
        db_assignment = db.query(TaskAssignment).filter(TaskAssignment.id == assignment_id).first()
        if not db_assignment:
            return None
            
        for key, value in assignment.model_dump(exclude_unset=True).items():
            setattr(db_assignment, key, value)
            
        # 如果任务完成，更新任务状态
        if assignment.status == '已完成':
            task = db.query(Task).filter(Task.id == db_assignment.task_id).first()
            if task:
                # 检查是否所有分配都已完成
                all_assignments = db.query(TaskAssignment).filter(
                    TaskAssignment.task_id == db_assignment.task_id
                ).all()
                
                if all(a.status == '已完成' for a in all_assignments):
                    task.status = '已完成'
                    
        db.commit()
        db.refresh(db_assignment)
        return db_assignment
    
    @staticmethod
    def delete_assignment(db: Session, assignment_id: int) -> bool:
        """删除任务分配"""
        db_assignment = db.query(TaskAssignment).filter(TaskAssignment.id == assignment_id).first()
        if not db_assignment:
            return False
            
        task_id = db_assignment.task_id
        db.delete(db_assignment)
        
        # 检查任务是否还有其他分配，如果没有则更新状态为未分配
        remaining_assignments = db.query(TaskAssignment).filter(
            TaskAssignment.task_id == task_id
        ).count()
        
        if remaining_assignments == 0:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = '未分配'
                
        db.commit()
        return True
    
    @staticmethod
    def get_user_task_stats(db: Session, user_id: int) -> dict:
        """获取用户任务统计"""
        assignments = db.query(TaskAssignment).filter(TaskAssignment.user_id == user_id).all()
        
        total = len(assignments)
        completed = len([a for a in assignments if a.status == '已完成'])
        in_progress = len([a for a in assignments if a.status == '进行中'])
        
        avg_score = 0
        if assignments:
            scores = [a.performance_score for a in assignments if a.performance_score > 0]
            if scores:
                avg_score = sum(scores) / len(scores)
        
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "in_progress_tasks": in_progress,
            "average_score": round(avg_score, 2)
        }
    
    @staticmethod
    def get_all_task_stats(db: Session) -> dict:
        """获取全部任务分配统计"""
        assignments = db.query(TaskAssignment).all()
        
        total = len(assignments)
        completed = len([a for a in assignments if a.status == '已完成'])
        in_progress = len([a for a in assignments if a.status == '进行中'])
        paused = len([a for a in assignments if a.status == '已暂停'])
        
        avg_progress = 0
        if assignments:
            progress_values = [a.progress for a in assignments]
            avg_progress = sum(progress_values) / len(progress_values)
        
        return {
            "total_assignments": total,
            "completed": completed,
            "in_progress": in_progress,
            "paused": paused,
            "avg_progress": round(avg_progress, 2)
        } 