#!/usr/bin/env python3
"""
PDF客户端服务示例
监听8800端口，接收后端发送的PDF预览请求，下载并打开PDF文件
"""

import json
import os
import subprocess
import sys
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import platform
import tempfile
import threading

class PDFPreviewHandler(BaseHTTPRequestHandler):
    """处理PDF预览请求的HTTP处理器"""
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/pdf-preview':
            self.handle_pdf_preview()
        else:
            self.send_error(404, "Not Found")
    
    def handle_pdf_preview(self):
        """处理PDF预览请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # 解析JSON数据
            pdf_data = json.loads(body.decode('utf-8'))
            print(f"\n📥 收到PDF预览请求:")
            print(f"   动作: {pdf_data.get('action')}")
            print(f"   文件名: {pdf_data['data']['filename']}")
            print(f"   下载URL: {pdf_data['data']['download_url']}")
            print(f"   文件大小: {pdf_data['data']['file_size']} bytes")
            print(f"   请求者: {pdf_data['data']['requester']['username']}")
            
            # 发送成功响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "PDF预览请求已接收",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
            # 在新线程中处理PDF下载和打开
            download_thread = threading.Thread(
                target=self.download_and_open_pdf,
                args=(pdf_data,)
            )
            download_thread.daemon = True
            download_thread.start()
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {e}")
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            print(f"❌ 处理请求时出错: {e}")
            self.send_error(500, str(e))
    
    def download_and_open_pdf(self, pdf_data):
        """下载并打开PDF文件"""
        try:
            # 提取必要信息
            filename = pdf_data['data']['filename']
            download_url = pdf_data['data']['download_url']
            
            # 创建临时目录存储PDF
            temp_dir = os.path.join(tempfile.gettempdir(), 'ACO_PDF_Preview')
            os.makedirs(temp_dir, exist_ok=True)
            
            # 构建本地文件路径
            local_path = os.path.join(temp_dir, filename)
            
            print(f"\n📥 开始下载PDF文件...")
            print(f"   URL: {download_url}")
            print(f"   保存到: {local_path}")
            
            # 下载PDF文件
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # 保存文件
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ PDF文件下载成功!")
            print(f"   文件大小: {os.path.getsize(local_path)} bytes")
            
            # 打开PDF文件
            self.open_pdf_file(local_path)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 下载PDF失败: {e}")
        except Exception as e:
            print(f"❌ 处理PDF文件时出错: {e}")
    
    def open_pdf_file(self, file_path):
        """使用系统默认程序打开PDF文件"""
        try:
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            elif system == 'Windows':
                os.startfile(file_path)
            elif system == 'Linux':
                subprocess.call(['xdg-open', file_path])
            else:
                print(f"⚠️ 不支持的操作系统: {system}")
                print(f"   请手动打开文件: {file_path}")
            
            print(f"✅ 已使用系统默认程序打开PDF文件")
            
        except Exception as e:
            print(f"❌ 打开PDF文件失败: {e}")
            print(f"   请手动打开文件: {file_path}")
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def run_server(port=8800):
    """运行PDF客户端服务"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, PDFPreviewHandler)
    
    print(f"🚀 PDF客户端服务已启动")
    print(f"   监听端口: {port}")
    print(f"   等待接收PDF预览请求...")
    print(f"   按 Ctrl+C 停止服务\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n⏹️  正在停止服务...")
        httpd.shutdown()
        print("👋 服务已停止")


if __name__ == '__main__':
    # 检查是否安装了requests库
    try:
        import requests
    except ImportError:
        print("❌ 缺少依赖库 'requests'")
        print("   请运行: pip install requests")
        sys.exit(1)
    
    # 运行服务
    run_server() 