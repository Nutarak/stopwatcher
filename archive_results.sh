#!/bin/bash

# 生成日期目录名（如 2025-06-14）
today=$(date '+%Y-%m-%d')
archive_dir="results/$today"

# 创建目录
mkdir -p "$archive_dir"

# 移动 .csv 和 .log 文件
echo "📦 正在归档结果文件到 $archive_dir"
mv *.csv *.log "$archive_dir/" 2>/dev/null

# 显示结果
echo "✅ 已归档以下文件："
ls -lh "$archive_dir"

