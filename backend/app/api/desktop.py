from fastapi import APIRouter

router = APIRouter(prefix="/api/desktop", tags=["desktop"])

@router.get("/test")
async def test_desktop():
    """测试桌面管理接口"""
    return {"message": "桌面管理模块正常工作"} 