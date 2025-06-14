#!/bin/bash

echo "🧹 正在清理调试数据文件 (*.csv 中含 _debug 的)..."

# 统计目标文件数量
count=$(ls *_debug.csv 2>/dev/null | wc -l)

if [ "$count" -eq 0 ]; then
    echo "✅ 当前没有可清理的 _debug.csv 文件"
    exit 0
fi

# 执行删除
rm *_debug.csv

echo "✅ 已删除 $count 个调试数据文件："
ls -1 *_debug.csv 2>/dev/null || echo "(所有目标文件已清除)"

