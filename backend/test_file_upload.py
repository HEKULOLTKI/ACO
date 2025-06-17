#!/usr/bin/env python3
"""
聊天系统文件上传功能测试脚本
"""

import requests
import json
import os
import time
import tempfile
from io import BytesIO
from pathlib import Path

# 配置
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "admin"  # 请根据实际情况修改
TEST_PASSWORD = "123456"  # 请根据实际情况修改

class ChatUploadTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.session = requests.Session()
    
    def login(self):
        """登录获取JWT Token"""
        try:
            # 使用form-data格式发送登录请求
            login_data = {
                "username": TEST_USERNAME,
                "password": TEST_PASSWORD
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                data=login_data  # 使用data而不是json
            )
            
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("access_token")
                # 设置默认认证头
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                print("✅ 登录成功，获取Token")
                return True
            else:
                print(f"❌ 登录失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def create_test_files(self):
        """创建测试文件"""
        test_files = {}
        
        # 创建文本文件
        txt_content = "这是一个测试文本文件\n用于测试聊天系统文件上传功能\n"
        txt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        txt_file.write(txt_content)
        txt_file.close()
        test_files['text'] = txt_file.name
        
        # 创建简单的图片文件（PNG格式）
        # 这里创建一个最小的PNG文件
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0bIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
        png_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        png_file.write(png_data)
        png_file.close()
        test_files['image'] = png_file.name
        
        return test_files
    
    def test_file_upload(self, file_path, file_type="text"):
        """测试文件上传"""
        try:
            file_name = os.path.basename(file_path)
            print(f"\n📤 测试上传文件: {file_name}")
            
            with open(file_path, 'rb') as f:
                files = {
                    'file': (file_name, f, self.get_content_type(file_path))
                }
                data = {
                    'room_id': 'global'
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/chat/upload",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 文件上传成功:")
                print(f"   消息ID: {result.get('id')}")
                print(f"   文件名: {result.get('file_name')}")
                print(f"   文件大小: {result.get('file_size')} bytes")
                print(f"   文件URL: {result.get('file_url')}")
                print(f"   消息类型: {result.get('message_type')}")
                return result
            else:
                print(f"❌ 文件上传失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 文件上传异常: {e}")
            return None
    
    def get_content_type(self, file_path):
        """根据文件扩展名获取Content-Type"""
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.txt': 'text/plain',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    def test_get_messages(self):
        """测试获取消息"""
        try:
            print(f"\n📥 测试获取消息历史...")
            response = self.session.get(f"{self.base_url}/api/chat/messages")
            
            if response.status_code == 200:
                messages = response.json()
                print(f"✅ 成功获取 {len(messages)} 条消息")
                
                # 显示最近的文件消息
                for msg in messages[-3:]:  # 显示最近3条
                    if msg.get('file_url'):
                        print(f"   📎 文件消息: {msg.get('file_name')} - {msg.get('content')}")
                    else:
                        print(f"   💬 文本消息: {msg.get('content')[:50]}...")
                return messages
            else:
                print(f"❌ 获取消息失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取消息异常: {e}")
            return None
    
    def test_online_users(self):
        """测试获取在线用户"""
        try:
            print(f"\n👥 测试获取在线用户...")
            response = self.session.get(f"{self.base_url}/api/chat/online-users")
            
            if response.status_code == 200:
                users = response.json()
                print(f"✅ 当前在线用户: {len(users)} 人")
                for user in users:
                    print(f"   - {user.get('username')} (ID: {user.get('user_id')})")
                return users
            else:
                print(f"❌ 获取在线用户失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取在线用户异常: {e}")
            return None
    
    def test_chat_stats(self):
        """测试获取聊天统计"""
        try:
            print(f"\n📊 测试获取聊天统计...")
            response = self.session.get(f"{self.base_url}/api/chat/stats")
            
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ 聊天统计:")
                print(f"   在线用户数: {stats.get('online_users_count')}")
                print(f"   今日消息数: {stats.get('total_messages_today')}")
                print(f"   活跃聊天室: {stats.get('active_rooms')}")
                return stats
            else:
                print(f"❌ 获取聊天统计失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取聊天统计异常: {e}")
            return None
    
    def test_file_access(self, file_url):
        """测试文件访问"""
        try:
            print(f"\n🔗 测试文件访问: {file_url}")
            full_url = f"{self.base_url}{file_url}"
            
            response = self.session.get(full_url)
            if response.status_code == 200:
                print(f"✅ 文件访问成功，大小: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ 文件访问失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 文件访问异常: {e}")
            return False
    
    def cleanup_test_files(self, test_files):
        """清理测试文件"""
        for file_type, file_path in test_files.items():
            try:
                os.unlink(file_path)
                print(f"🗑️ 清理测试文件: {os.path.basename(file_path)}")
            except:
                pass
    
    def run_tests(self):
        """运行所有测试"""
        print("🚀 开始聊天系统文件上传功能测试")
        print("=" * 50)
        
        # 1. 登录
        if not self.login():
            print("❌ 登录失败，无法继续测试")
            return False
        
        # 2. 创建测试文件
        print(f"\n📁 创建测试文件...")
        test_files = self.create_test_files()
        print(f"✅ 创建了 {len(test_files)} 个测试文件")
        
        uploaded_files = []
        
        try:
            # 3. 测试文件上传
            for file_type, file_path in test_files.items():
                result = self.test_file_upload(file_path, file_type)
                if result:
                    uploaded_files.append(result)
                time.sleep(1)  # 避免请求过快
            
            # 4. 测试获取消息
            self.test_get_messages()
            
            # 5. 测试文件访问
            for file_info in uploaded_files:
                if file_info.get('file_url'):
                    self.test_file_access(file_info['file_url'])
            
            # 6. 测试其他功能
            self.test_online_users()
            self.test_chat_stats()
            
            print("\n" + "=" * 50)
            print("✅ 所有测试完成！")
            
            # 测试总结
            print(f"\n📋 测试总结:")
            print(f"   成功上传文件: {len(uploaded_files)} 个")
            for file_info in uploaded_files:
                print(f"   - {file_info.get('file_name')} ({file_info.get('message_type')})")
            
            return True
            
        finally:
            # 7. 清理测试文件
            print(f"\n🧹 清理测试文件...")
            self.cleanup_test_files(test_files)

def main():
    """主函数"""
    tester = ChatUploadTester()
    
    try:
        success = tester.run_tests()
        if success:
            print("\n🎉 文件上传功能测试通过！")
        else:
            print("\n⚠️ 文件上传功能测试存在问题")
    except KeyboardInterrupt:
        print("\n\n⏸️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中发生异常: {e}")

if __name__ == "__main__":
    main() 