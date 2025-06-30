#!/usr/bin/env python3
"""
数据库迁移脚本：增加knowledge_documents表中file_type字段长度
从VARCHAR(50)增加到VARCHAR(255)以支持长MIME类型
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
import pymysql

# 数据库配置 - 根据实际配置
DATABASE_URL = "mysql+pymysql://user:ChinaSkills!@localhost:3306/conlse_sql?charset=utf8mb4"

def migrate_file_type_length():
    """增加file_type字段长度"""
    print("开始迁移file_type字段长度...")
    
    # 创建数据库连接
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.begin() as conn:
            # 检查当前字段长度
            print("检查当前字段定义...")
            result = conn.execute(text("""
                SELECT DATA_TYPE, CHARACTER_MAXIMUM_LENGTH 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'knowledge_documents' 
                AND COLUMN_NAME = 'file_type'
            """))
            
            current_info = result.fetchone()
            if current_info:
                print(f"当前字段类型: {current_info[0]}, 长度: {current_info[1]}")
                
                if current_info[1] == 50:
                    print("执行字段长度修改...")
                    # 修改字段长度
                    conn.execute(text("""
                        ALTER TABLE knowledge_documents 
                        MODIFY COLUMN file_type VARCHAR(255) COMMENT '文件类型'
                    """))
                    print("✅ file_type字段长度已成功增加到255")
                else:
                    print(f"字段长度已经是{current_info[1]}，无需修改")
            else:
                print("❌ 未找到file_type字段")
                
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        raise
    
    print("迁移完成！")

if __name__ == "__main__":
    migrate_file_type_length() 