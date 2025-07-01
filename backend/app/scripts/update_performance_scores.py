#!/usr/bin/env python3
"""
更新绩效评分脚本
确保现有任务的绩效评分符合新的业务规则：只有进度达到100%的任务才能获得100分
"""

import sys
import os

# 添加父目录到路径，以便导入app模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.task import TaskAssignment

def update_performance_scores():
    """更新所有任务分配的绩效评分"""
    # 创建数据库会话
    db = Session(engine)
    
    try:
        # 获取所有任务分配
        assignments = db.query(TaskAssignment).all()
        
        updated_count = 0
        
        for assignment in assignments:
            original_score = assignment.performance_score
            should_update = False
            
            # 如果进度小于100%但绩效评分超过进度值，需要调整
            if assignment.progress < 100 and assignment.performance_score > assignment.progress:
                assignment.performance_score = assignment.progress
                should_update = True
                print(f"任务分配ID {assignment.id}: 进度{assignment.progress}%，绩效评分从{original_score}分调整为{assignment.performance_score}分")
            
            # 如果进度达到100%且状态为已完成，但绩效评分不是100分，可以设置为100分
            elif assignment.progress == 100 and assignment.status == '已完成' and assignment.performance_score != 100:
                assignment.performance_score = 100
                should_update = True
                print(f"任务分配ID {assignment.id}: 进度100%且已完成，绩效评分从{original_score}分调整为100分")
            
            if should_update:
                updated_count += 1
        
        # 提交更改
        db.commit()
        print(f"\n更新完成！共更新了 {updated_count} 个任务分配的绩效评分")
        
    except Exception as e:
        print(f"更新过程中出现错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("开始更新绩效评分...")
    update_performance_scores()
    print("脚本执行完成！") 