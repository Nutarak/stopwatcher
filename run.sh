#!/bin/bash

# 进入项目目录
cd "$(dirname "$0")"

# 启动调试日志
echo "=== [$(date)] Cron Running run.sh ===" >> cron_debug.log

# 激活虚拟环境
source venv/bin/activate

# 写入 Python 路径与依赖确认
which python >> cron_debug.log
python -m pip list | grep -E 'yfinance|requests' >> cron_debug.log

# 执行主程序 + 写入主运行日志
python watcher.py >> monitor_log.txt 2>&1

