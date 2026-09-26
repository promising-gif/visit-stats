# 网站访问统计系统

一个轻量级的网站访问统计系统，支持埋点自动上报、数据持久化和可视化展示。

## 技术栈

- 后端：Python + FastAPI + SQLAlchemy
- 数据库：MySQL
- 前端：原生 HTML + CSS + JavaScript
- 部署：ngrok 内网穿透

## 功能

- 埋点自动上报：网页加载时自动发送访问记录
- 实时看板：展示总访问量、今日访问量、热门页面排行
- 日期筛选：按日期查看访问记录
- 公网访问：支持跨网络访问
- 🤖 AI 智能分析：集成 DeepSeek API，自动分析访问数据并生成优化建议

## 快速开始

1. 安装依赖：
   pip install fastapi uvicorn sqlalchemy pymysql python-dotenv

2. 配置 `.env` 文件：
   DATABASE_URL="mysql+pymysql://root:你的密码@localhost:3306/test_db"

3. 启动服务：
   uvicorn main:app --reload

4. 打开看板：
   浏览器访问 http://127.0.0.1:8000

## 项目结构

- `main.py`：后端主程序，包含所有 API 接口
- `pandas_demo.py`：用 Pandas 对访问数据做分析
- `predict_demo.py`：PyTorch 手写数字分类 Demo
- `main.py`：后端主程序，包含所有 API 接口和 AI 分析功能

## 项目截图

![统计看板截图](dashboard.png)