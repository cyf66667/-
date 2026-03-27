# 使用轻量级的 Python 3.10 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 把当前目录下的所有代码复制到容器内
COPY . .

# 暴露 8000 端口（给 FastAPI 用）
EXPOSE 8000