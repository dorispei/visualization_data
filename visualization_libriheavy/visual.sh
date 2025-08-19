#!/bin/bash

# 配置参数
APP_PATH="./visualization/streamlit_list_viz.py"       # 你的 Streamlit 脚本路径
PORT=8501               # Streamlit 端口

# 1️⃣ 启用 UFW 防火墙（如果没启用）
echo "启用 UFW 防火墙..."
sudo ufw enable || echo "UFW 已启用或无法启用"

# 2️⃣ 允许 8501 端口 TCP 访问
echo "放行端口 $PORT..."
sudo ufw allow ${PORT}/tcp

# 3️⃣ 显示防火墙状态
sudo ufw status

# 4️⃣ 启动 Streamlit
echo "启动 Streamlit..."
streamlit run $APP_PATH --server.address 0.0.0.0 --server.port $PORT --server.headless true
