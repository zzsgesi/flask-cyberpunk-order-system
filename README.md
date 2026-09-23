# flask-cyberpunk-order-system

## 项目简介

基于 Flask 框架的赛博朋克主题义体订单管理系统，模拟夜之城义体医生的订单处理流程。项目包含用户登录鉴权、订单增删查、VIP 等级展示、Redis 异步任务队列与后台 Worker 消费，是一个完整的 Web 后端实践项目。

## 技术栈

- Python
- Flask
- Redis（异步任务队列）
- MySQL（数据持久化）
- DBUtils（数据库连接池）
- Jinja2（模板渲染）
- HTML / CSS

## 功能说明

- 用户登录与角色鉴权（管理员 / 客户），基于 Session 实现访问控制
- 订单管理：创建订单、查看订单列表、删除订单
- VIP 等级展示：根据用户 VIP 等级渲染不同身份标识
- Redis 队列：下单后将订单 ID 推入 Redis 队列，由后台 Worker 异步消费
- 订单状态流转：待执行 → 正在执行 → 完成 / 失败
- 断点恢复：Worker 启动时自动对比 MySQL 与 Redis，补齐未完成的订单

## 运行方式

1. 安装依赖：
   ```bash
   pip install flask redis pymysql dbutils
2. 启动 MySQL 与 Redis 服务，并创建数据库 flask_project_db
3. 修改 utils/db.py 和 worker.py 中的数据库连接配置（host、user、password、db）
4. 启动 Flask 应用：python app.py
5. 另开一个终端，启动后台 Worker：python worker.py
6. 浏览器访问 http://127.0.0.1:5000/home

## 运行结果
- 用户可登录并进入义体订单管理界面
- 创建订单后，订单 ID 被推入 Redis 队列
- 后台 Worker 异步消费订单，更新订单状态
- 支持订单列表查看与删除
