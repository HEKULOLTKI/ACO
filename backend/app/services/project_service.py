from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
import pandas as pd
import io
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    """项目服务类"""
    
    @staticmethod
    def create_project(db: Session, project_data: ProjectCreate) -> Project:
        """创建项目"""
        db_project = Project(
            name=project_data.name,
            description=project_data.description,
            status=project_data.status,
            icon=project_data.icon
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
        """获取所有项目"""
        return db.query(Project).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_project(db: Session, project_id: int) -> Optional[Project]:
        """通过ID获取项目"""
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def get_project_by_name(db: Session, name: str) -> Optional[Project]:
        """通过名称获取项目"""
        return db.query(Project).filter(Project.name == name).first()
    
    @staticmethod
    def update_project(db: Session, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
        """更新项目"""
        db_project = ProjectService.get_project(db, project_id)
        if not db_project:
            return None
            
        update_data = project_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
            
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        """删除项目"""
        db_project = ProjectService.get_project(db, project_id)
        if not db_project:
            return False
            
        db.delete(db_project)
        db.commit()
        return True
    
    @staticmethod
    def import_projects_from_excel(db: Session, file_content: bytes) -> Dict[str, Any]:
        """从Excel导入项目"""
        try:
            # 读取Excel文件
            df = pd.read_excel(io.BytesIO(file_content))
            
            required_columns = ['name', 'description']
            # 验证必需列
            for col in required_columns:
                if col not in df.columns:
                    return {
                        "success_count": 0,
                        "fail_count": 0,
                        "failed_projects": [],
                        "message": f"Excel文件缺少必需列: {col}"
                    }
                    
            success_count = 0
            fail_count = 0
            failed_projects = []
            
            # 处理每一行数据
            for _, row in df.iterrows():
                try:
                    # 提取项目数据
                    project_data = {
                        "name": str(row["name"]).strip(),
                        "description": str(row.get("description", "")) if not pd.isna(row.get("description", "")) else "",
                        "status": str(row.get("status", "开发中")) if not pd.isna(row.get("status", "")) else "开发中",
                        "icon": str(row.get("icon", "Briefcase")) if not pd.isna(row.get("icon", "")) else "Briefcase",
                        "manager_id": int(row["manager_id"]) if "manager_id" in row and not pd.isna(row["manager_id"]) else None,
                        "planning": str(row.get("planning", "")) if not pd.isna(row.get("planning", "")) else None
                    }
                    
                    # 检查项目是否已存在
                    existing_project = ProjectService.get_project_by_name(db, project_data["name"])
                    if existing_project:
                        failed_projects.append({
                            "name": project_data["name"],
                            "error": "项目名称已存在"
                        })
                        fail_count += 1
                        continue
                    
                    # 创建新项目
                    ProjectService.create_project(db, ProjectCreate(**project_data))
                    success_count += 1
                    
                except Exception as e:
                    # 记录失败信息
                    failed_projects.append({
                        "name": row.get("name", "未知"),
                        "error": str(e)
                    })
                    fail_count += 1
            
            # 返回导入结果
            return {
                "success_count": success_count,
                "fail_count": fail_count,
                "failed_projects": failed_projects,
                "message": f"导入完成: {success_count}个成功, {fail_count}个失败"
            }
            
        except Exception as e:
            return {
                "success_count": 0,
                "fail_count": 0,
                "failed_projects": [],
                "message": f"导入失败: {str(e)}"
            } 