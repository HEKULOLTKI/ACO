#!/usr/bin/env python3
"""
测试API端点是否正确注册
"""
import requests
import sys

BASE_URL = "http://localhost:8000"

def test_system_endpoints():
    """测试系统API端点"""
    print("🧪 测试系统API端点...")
    
    # 测试无需认证的端点
    endpoints_no_auth = [
        ("/api/system/health", "GET"),
        ("/", "GET"),
        ("/health", "GET")
    ]
    
    for endpoint, method in endpoints_no_auth:
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
            
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {str(e)}")
    
    print()
    
    # 测试需要认证的端点（预期会返回401）
    endpoints_auth_required = [
        ("/api/system/status", "GET"),
        ("/api/system/stats", "GET"),
        ("/api/system/reports", "GET"),
        ("/api/system/reports/generate", "POST")
    ]
    
    print("🔐 测试需要认证的端点（预期401状态码）...")
    
    for endpoint, method in endpoints_auth_required:
        try:
            url = f"{BASE_URL}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, timeout=5)
            
            if response.status_code == 401:
                print(f"✅ {method} {endpoint} - Status: {response.status_code} (需要认证)")
            elif response.status_code == 404:
                print(f"❌ {method} {endpoint} - Status: {response.status_code} (端点未找到)")
            else:
                print(f"⚠️  {method} {endpoint} - Status: {response.status_code} (异常状态)")
                
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {str(e)}")

def test_openapi_docs():
    """测试OpenAPI文档"""
    print("\n📖 测试API文档...")
    
    try:
        # 测试OpenAPI JSON
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            print("✅ OpenAPI JSON 可访问")
            
            # 检查是否包含报告端点
            openapi_data = response.json()
            paths = openapi_data.get('paths', {})
            
            report_endpoints = [
                '/api/system/reports/generate',
                '/api/system/reports',
                '/api/system/reports/download/{filename}'
            ]
            
            print("\n🔍 检查报告端点是否在OpenAPI中注册:")
            for endpoint in report_endpoints:
                if endpoint in paths:
                    print(f"✅ {endpoint} - 已注册")
                else:
                    print(f"❌ {endpoint} - 未注册")
                    
        else:
            print(f"❌ OpenAPI JSON 访问失败 - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ OpenAPI JSON 测试失败: {str(e)}")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 API端点测试")
    print("=" * 60)
    
    try:
        # 首先检查服务器是否运行
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ 服务器运行正常 - Status: {response.status_code}")
        print()
        
        test_system_endpoints()
        test_openapi_docs()
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 测试完成")

if __name__ == "__main__":
    main() 