# ⏰ StopWatcher - 自动止盈止损监控系统

> 实时追踪股票价格、触发止盈止损条件，并通过 Telegram 通知你！

---

## 📌 项目简介

`StopWatcher` 是一个轻量级的命令行工具，用于监控多支股票的价格波动。当股票价格达到设定的止盈或止损区间时，自动通过 Telegram 向你推送通知，避免你错过重要时机。

---

## ⚙️ 功能特性

- ✅ 支持美股、日股等主流股票市场（数据源：Yahoo Finance）
- 🎯 每支股票支持设置独立的：
  - 买入价
  - 止盈百分比
  - 止损百分比
- 🔕 自动避免重复提醒（每日仅提醒一次）
- 🔁 每日自动重置提醒状态
- 📲 使用 Telegram Bot 实时推送提醒
- 🖥️ 本地 Linux 系统运行，配合 crontab 实现定时执行

---

## 🚀 安装步骤

```bash
git clone git@github.com:Nutarak/stopwatcher.git
cd stopwatcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
