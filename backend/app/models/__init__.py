"""
数据模型包
导入所有数据模型类
"""

from .user import User
from .task import Task, TaskAssignment
from .device import Device
from .desktop import DesktopItem, ToolboxTool
from .system import SystemSettings
from .knowledge import KnowledgeBase, KnowledgeDocument, AIModel

# 导出所有模型
__all__ = [
    "User",
    "Task",
    "TaskAssignment", 
    "Device",
    "DesktopItem",
    "ToolboxTool",  # 注意：ToolboxTool已移除user_id外键关联
    "SystemSettings",
    "KnowledgeBase",
    "KnowledgeDocument",
    "AIModel"
] 