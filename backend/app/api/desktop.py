from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.desktop import DesktopItem, ToolboxTool
from app.schemas.desktop import (
    DesktopItemCreate, DesktopItemUpdate, DesktopItemResponse,
    ToolboxToolCreate, ToolboxToolUpdate, ToolboxToolResponse
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/desktop")

# 桌面项目管理
@router.get("/items", response_model=List[DesktopItemResponse])
async def get_desktop_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的桌面项目列表"""
    items = db.query(DesktopItem).filter(DesktopItem.user_id == current_user.id).all()
    return items

@router.post("/items", response_model=DesktopItemResponse)
async def create_desktop_item(
    item_data: DesktopItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的桌面项目"""
    # 创建桌面项目
    db_item = DesktopItem(
        name=item_data.name,
        type=item_data.type,
        path=item_data.path,
        icon=item_data.icon,
        role=item_data.role,
        position_x=item_data.position_x,
        position_y=item_data.position_y,
        user_id=current_user.id
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/{item_id}", response_model=DesktopItemResponse)
async def get_desktop_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定的桌面项目"""
    item = db.query(DesktopItem).filter(
        DesktopItem.id == item_id,
        DesktopItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="桌面项目不存在"
        )
    
    return item

@router.put("/items/{item_id}", response_model=DesktopItemResponse)
async def update_desktop_item(
    item_id: int,
    item_data: DesktopItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新桌面项目"""
    item = db.query(DesktopItem).filter(
        DesktopItem.id == item_id,
        DesktopItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="桌面项目不存在"
        )
    
    # 更新字段
    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item

@router.delete("/items/{item_id}")
async def delete_desktop_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除桌面项目"""
    item = db.query(DesktopItem).filter(
        DesktopItem.id == item_id,
        DesktopItem.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="桌面项目不存在"
        )
    
    db.delete(item)
    db.commit()
    return {"message": "桌面项目删除成功"}

# 工具箱管理
@router.get("/tools", response_model=List[ToolboxToolResponse])
async def get_toolbox_tools(db: Session = Depends(get_db)):
    """获取工具箱工具列表"""
    tools = db.query(ToolboxTool).all()
    return tools

@router.post("/tools", response_model=ToolboxToolResponse)
async def create_toolbox_tool(
    tool_data: ToolboxToolCreate,
    db: Session = Depends(get_db)
):
    """创建新的工具箱工具"""
    db_tool = ToolboxTool(
        name=tool_data.name,
        command=tool_data.command,
        icon=tool_data.icon
    )
    
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

@router.put("/tools/{tool_id}", response_model=ToolboxToolResponse)
async def update_toolbox_tool(
    tool_id: int,
    tool_data: ToolboxToolUpdate,
    db: Session = Depends(get_db)
):
    """更新工具箱工具"""
    tool = db.query(ToolboxTool).filter(ToolboxTool.id == tool_id).first()
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工具不存在"
        )
    
    # 更新字段
    update_data = tool_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tool, field, value)
    
    db.commit()
    db.refresh(tool)
    return tool

@router.delete("/tools/{tool_id}")
async def delete_toolbox_tool(
    tool_id: int,
    db: Session = Depends(get_db)
):
    """删除工具箱工具"""
    tool = db.query(ToolboxTool).filter(ToolboxTool.id == tool_id).first()
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工具不存在"
        )
    
    db.delete(tool)
    db.commit()
    return {"message": "工具删除成功"}

@router.get("/test")
async def test_desktop():
    """测试桌面管理接口"""
    return {"message": "桌面管理模块正常工作"} 