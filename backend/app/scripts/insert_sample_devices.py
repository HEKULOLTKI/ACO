"""
插入示例设备数据脚本
运行方式: python -m app.scripts.insert_sample_devices
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.device import Device
from sqlalchemy.orm import Session
from datetime import datetime

def insert_sample_devices():
    """插入示例设备数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有设备数据
        existing_count = db.query(Device).count()
        if existing_count > 0:
            print(f"✅ 数据库中已有 {existing_count} 个设备，跳过插入示例数据")
            return
        
        # 示例设备数据
        sample_devices = [
            {
                "name": "Web服务器001",
                "type": "服务器",
                "ip": "192.168.1.100",
                "status": "online",
                "location": "机房A-机柜01"
            },
            {
                "name": "Web服务器002",
                "type": "服务器",
                "ip": "192.168.1.101",
                "status": "online",
                "location": "机房A-机柜02"
            },
            {
                "name": "DB服务器001",
                "type": "数据库服务器",
                "ip": "192.168.1.200",
                "status": "online",
                "location": "机房B-机柜01"
            },
            {
                "name": "核心交换机001",
                "type": "交换机",
                "ip": "192.168.1.10",
                "status": "online",
                "location": "机房A-网络区"
            },
            {
                "name": "核心交换机002",
                "type": "交换机",
                "ip": "192.168.1.11",
                "status": "offline",
                "location": "机房B-网络区"
            },
            {
                "name": "防火墙001",
                "type": "安全设备",
                "ip": "192.168.1.1",
                "status": "online",
                "location": "机房A-安全区"
            },
            {
                "name": "负载均衡器001",
                "type": "负载均衡器",
                "ip": "192.168.1.50",
                "status": "online",
                "location": "机房A-网络区"
            },
            {
                "name": "存储服务器001",
                "type": "存储设备",
                "ip": "192.168.1.150",
                "status": "maintenance",
                "location": "机房B-存储区"
            },
            {
                "name": "监控服务器001",
                "type": "监控设备",
                "ip": "192.168.1.250",
                "status": "online",
                "location": "机房A-管理区"
            },
            {
                "name": "备份服务器001",
                "type": "备份设备",
                "ip": "192.168.1.251",
                "status": "error",
                "location": "机房B-备份区"
            }
        ]
        
        # 插入设备数据
        inserted_count = 0
        for device_data in sample_devices:
            device = Device(**device_data)
            db.add(device)
            inserted_count += 1
        
        db.commit()
        print(f"✅ 成功插入 {inserted_count} 个示例设备")
        
        # 显示统计信息
        total_devices = db.query(Device).count()
        online_devices = db.query(Device).filter(Device.status == 'online').count()
        offline_devices = db.query(Device).filter(Device.status == 'offline').count()
        maintenance_devices = db.query(Device).filter(Device.status == 'maintenance').count()
        error_devices = db.query(Device).filter(Device.status == 'error').count()
        
        print(f"📊 设备统计:")
        print(f"   总设备数: {total_devices}")
        print(f"   在线设备: {online_devices}")
        print(f"   离线设备: {offline_devices}")
        print(f"   维护设备: {maintenance_devices}")
        print(f"   故障设备: {error_devices}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 插入示例设备数据失败: {str(e)}")
        raise
    finally:
        db.close()

def main():
    """主函数"""
    print("🚀 开始插入示例设备数据...")
    insert_sample_devices()
    print("✅ 示例设备数据插入完成！")

if __name__ == "__main__":
    main() 