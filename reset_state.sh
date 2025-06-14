#!/bin/bash
# 清空状态记录文件 state.json
STATE_FILE="$(dirname "$0")/state.json"

if [ -f "$STATE_FILE" ]; then
    echo "{}" > "$STATE_FILE"
    echo "[reset_state] 状态已清空 ✅"
else
    echo "[reset_state] 无需清空，state.json 不存在。"
fi
