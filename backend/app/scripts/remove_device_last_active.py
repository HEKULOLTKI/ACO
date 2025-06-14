"""
数据库迁移脚本：删除设备表的last_active字段
运行方式: python -m app.scripts.remove_device_last_active
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.config import settings

def remove_device_last_active_column():
    """删除设备表的last_active字段"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        # 检查last_active列是否存在
        check_column_sql = """
        SELECT COUNT(*) as count
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'devices'
        AND COLUMN_NAME = 'last_active'
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(check_column_sql))
            column_exists = result.fetchone()[0] > 0
            
            if not column_exists:
                print("✅ 设备表last_active字段不存在，无需删除")
                return
            
            # 删除last_active字段
            drop_column_sql = """
            ALTER TABLE devices 
            DROP COLUMN last_active
            """
            
            connection.execute(text(drop_column_sql))
            connection.commit()
            
            print("✅ 成功删除设备表last_active字段")
            
    except Exception as e:
        print(f"❌ 删除last_active字段失败: {str(e)}")
        raise

def main():
    """主函数"""
    print("🚀 开始删除设备表last_active字段...")
    
    # 删除last_active字段
    remove_device_last_active_column()
    
    print("✅ 设备表结构迁移完成！")

if __name__ == "__main__":
    main() 