#!/bin/bash

echo "🔄 开始 Git 同步..."

# 拉取远程变更
git pull origin main

# 添加所有更改文件
git add .

# 自动生成提交信息
commit_msg="自动更新：$(date '+%Y-%m-%d %H:%M')"
git commit -m "$commit_msg"

# 推送到远程仓库
git push origin main

echo "✅ Git 同步完成：$commit_msg"

