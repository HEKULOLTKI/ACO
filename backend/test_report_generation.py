#!/usr/bin/env python3
"""
测试项目报告生成功能
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api.system import create_project_report_pdf

async def test_report_generation():
    """测试报告生成功能"""
    print("🧪 开始测试项目报告生成功能...")
    
    # 创建测试数据
    test_data = {
        "report_title": "多智能体协作运维系统项目报告",
        "generated_at": datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"),
        "generated_by": "测试用户",
        "system_overview": {
            "total_users": 10,
            "total_tasks": 25,
            "total_devices": 8
        },
        "task_statistics": {
            "pending": 3,
            "running": 8,
            "completed": 12,
            "failed": 2
        },
        "device_statistics": {
            "online": 6,
            "offline": 2
        }
    }
    
    # 创建输出目录
    reports_dir = Path("uploads/progress_reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成测试报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"测试报告_{timestamp}.pdf"
    pdf_path = reports_dir / pdf_filename
    
    try:
        print(f"📄 正在生成报告: {pdf_filename}")
        await create_project_report_pdf(test_data, pdf_path)
        
        if pdf_path.exists():
            file_size = pdf_path.stat().st_size
            print(f"✅ 报告生成成功!")
            print(f"📁 文件路径: {pdf_path}")
            print(f"📊 文件大小: {file_size} 字节")
            print(f"🌐 访问URL: http://localhost:8000/uploads/progress_reports/{pdf_filename}")
            return True
        else:
            print("❌ 报告文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ 报告生成失败: {str(e)}")
        return False

async def list_existing_reports():
    """列出现有报告"""
    print("\n📋 现有报告列表:")
    reports_dir = Path("uploads/progress_reports")
    
    if not reports_dir.exists():
        print("❌ 报告目录不存在")
        return
    
    pdf_files = list(reports_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("📭 暂无PDF报告文件")
    else:
        for pdf_file in pdf_files:
            stat = pdf_file.stat()
            size_mb = stat.st_size / (1024 * 1024)
            created_time = datetime.fromtimestamp(stat.st_ctime)
            print(f"📄 {pdf_file.name}")
            print(f"   大小: {size_mb:.2f} MB")
            print(f"   创建时间: {created_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   访问URL: http://localhost:8000/uploads/progress_reports/{pdf_file.name}")
            print()

async def main():
    """主函数"""
    print("=" * 60)
    print("🚀 项目报告生成功能测试")
    print("=" * 60)
    
    # 列出现有报告
    await list_existing_reports()
    
    # 测试报告生成
    success = await test_report_generation()
    
    if success:
        print("\n🎉 测试完成！您可以通过以下方式访问报告:")
        print("1. 直接访问生成的URL")
        print("2. 在任务进度页面点击'查看报告列表'按钮")
        print("3. 在任务进度页面点击'生成项目报告'按钮")
    else:
        print("\n❌ 测试失败，请检查错误信息")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 