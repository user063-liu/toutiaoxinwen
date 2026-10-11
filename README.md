# 头条新闻（toutiaoxinwen）后端接口

这是“头条新闻”项目的后端代码。

## 🛠️ 技术栈
- Python
- FastAPI
- SQLAlchemy
- MySQL

## 📂 项目结构
- `config/`：数据库等配置
- `crud/`：数据库增删改查逻辑
- `models/`：数据库表模型
- `routers/`：API 路由接口
- `schemas/`：数据校验模型
- `utils/`：工具类和通用方法
- `main.py`：项目启动入口

## 🚀 如何运行
1. 安装依赖：
   `pip install -r requirements.txt`（如果还没有这个文件，可以自己生成一个）
2. 配置数据库：
   修改 `config/db_conf.py` 里的数据库连接信息。
3. 启动服务：
   `python main.py` 或者 `uvicorn main:app --reload`