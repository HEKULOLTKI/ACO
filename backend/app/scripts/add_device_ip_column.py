"""
数据库迁移脚本：为设备表添加IP字段
运行方式: python -m app.scripts.add_device_ip_column
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.config import settings
from app.database import SessionLocal

def add_device_ip_column():
    """为设备表添加IP字段"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        # 检查IP列是否已经存在
        check_column_sql = """
        SELECT COUNT(*) as count
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'devices'
        AND COLUMN_NAME = 'ip'
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(check_column_sql))
            column_exists = result.fetchone()[0] > 0
            
            if column_exists:
                print("✅ 设备表IP字段已存在，无需添加")
                return
            
            # 添加IP字段
            add_column_sql = """
            ALTER TABLE devices 
            ADD COLUMN ip VARCHAR(50) COMMENT '设备IP地址' 
            AFTER type
            """
            
            connection.execute(text(add_column_sql))
            connection.commit()
            
            print("✅ 成功为设备表添加IP字段")
            
    except Exception as e:
        print(f"❌ 添加IP字段失败: {str(e)}")
        raise

def create_device_indexes():
    """为设备表创建索引"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            # 为IP字段创建索引
            try:
                create_ip_index_sql = """
                CREATE INDEX idx_devices_ip ON devices(ip)
                """
                connection.execute(text(create_ip_index_sql))
                print("✅ 创建设备IP索引成功")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("✅ 设备IP索引已存在")
                else:
                    print(f"❌ 创建设备IP索引失败: {str(e)}")
            
            # 为设备名称创建索引
            try:
                create_name_index_sql = """
                CREATE INDEX idx_devices_name ON devices(name)
                """
                connection.execute(text(create_name_index_sql))
                print("✅ 创建设备名称索引成功")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("✅ 设备名称索引已存在")
                else:
                    print(f"❌ 创建设备名称索引失败: {str(e)}")
            
            # 为设备类型创建索引
            try:
                create_type_index_sql = """
                CREATE INDEX idx_devices_type ON devices(type)
                """
                connection.execute(text(create_type_index_sql))
                print("✅ 创建设备类型索引成功")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("✅ 设备类型索引已存在")
                else:
                    print(f"❌ 创建设备类型索引失败: {str(e)}")
            
            # 为设备状态创建索引
            try:
                create_status_index_sql = """
                CREATE INDEX idx_devices_status ON devices(status)
                """
                connection.execute(text(create_status_index_sql))
                print("✅ 创建设备状态索引成功")
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("✅ 设备状态索引已存在")
                else:
                    print(f"❌ 创建设备状态索引失败: {str(e)}")
            
            connection.commit()
            
    except Exception as e:
        print(f"❌ 创建索引失败: {str(e)}")

def main():
    """主函数"""
    print("🚀 开始设备表结构迁移...")
    
    # 添加IP字段
    add_device_ip_column()
    
    # 创建索引
    create_device_indexes()
    
    print("✅ 设备表结构迁移完成！")

if __name__ == "__main__":
    main() 