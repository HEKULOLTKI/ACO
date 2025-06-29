# PDF客户端服务

这是一个PDF客户端服务示例，用于接收后端发送的PDF预览请求并自动打开PDF文件。

## 功能说明

- 监听本地8800端口
- 接收后端发送的JSON格式的PDF预览请求
- 自动下载PDF文件到本地临时目录
- 使用系统默认PDF阅读器打开文件

## 安装依赖

```bash
pip install requests
```

## 运行客户端

```bash
python pdf_client.py
```

## 工作流程

1. 客户端启动并监听8800端口
2. 用户在Web界面点击"发送到客户端"按钮
3. 后端获取用户IP并发送JSON数据到客户端
4. 客户端接收JSON数据并解析
5. 客户端下载PDF文件到临时目录
6. 使用系统默认程序打开PDF文件

## JSON数据格式

客户端接收的JSON数据格式示例：

```json
{
    "action": "pdf_download_and_preview",
    "data": {
        "filename": "项目报告.pdf",
        "download_url": "http://localhost:8000/api/pdf/download/项目报告.pdf",
        "file_size": 1024000,
        "requester": {
            "username": "admin"
        }
    }
}
```

## 注意事项

1. 确保防火墙允许8800端口的入站连接
2. 客户端需要能够访问后端服务器下载PDF文件
3. 支持Windows、macOS和Linux系统
4. PDF文件会保存在系统临时目录的`ACO_PDF_Preview`文件夹中

## 故障排除

### 无法连接到客户端

- 检查客户端是否正在运行
- 确认防火墙设置允许8800端口
- 验证网络连接是否正常

### PDF无法打开

- 确保系统已安装PDF阅读器
- 检查文件是否下载完整
- 查看控制台输出的错误信息 