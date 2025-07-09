from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.project_service import ProjectService
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectImportResult
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/project", response_model=List[Project])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有项目"""
    return ProjectService.get_projects(db, skip, limit)

@router.post("/project", response_model=Project)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新项目"""
    # 检查项目名称是否已存在
    existing_project = ProjectService.get_project_by_name(db, project.name)
    if existing_project:
        raise HTTPException(status_code=400, detail="项目名称已存在")
        
    return ProjectService.create_project(db, project)

@router.get("/project/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定项目"""
    db_project = ProjectService.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_project

@router.put("/project/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目信息"""
    # 检查项目是否存在
    db_project = ProjectService.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 如果更改了名称，检查新名称是否已存在
    if project_update.name and project_update.name != db_project.name:
        existing_project = ProjectService.get_project_by_name(db, project_update.name)
        if existing_project:
            raise HTTPException(status_code=400, detail="项目名称已存在")
    
    updated_project = ProjectService.update_project(db, project_id, project_update)
    return updated_project

@router.delete("/project/{project_id}", response_model=Dict[str, Any])
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除项目"""
    # 检查项目是否存在
    db_project = ProjectService.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    success = ProjectService.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除项目失败")
    
    return {"success": True, "message": "项目已成功删除"}

@router.post("/project/import", response_model=ProjectImportResult)
async def import_projects(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从Excel文件导入项目"""
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="仅支持Excel文件格式(.xlsx, .xls)")
    
    # 读取文件内容
    file_content = await file.read()
    
    # 导入项目
    import_result = ProjectService.import_projects_from_excel(db, file_content)
    
    return import_result 