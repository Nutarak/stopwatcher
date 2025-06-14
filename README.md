# 📈 StopWatcher: ATR 动态止盈止损系统

**StopWatcher** 是一个基于 Python 的多资产止盈止损回测系统，利用 **ATR（Average True Range）** 进行波动率动态调节，适用于资产监控、回测分析与交易策略验证。

---

## 🚀 功能概览

- ✅ 自动下载美股历史数据（使用 `yfinance`）
- ✅ 计算 14 日 ATR 波动指标（通过 `pandas_ta`）
- ✅ 动态设定止盈 / 止损线（支持倍数配置）
- ✅ 模拟策略在过去一年中是否被触发
- ✅ 输出每日回测明细与总结报告（CSV 格式）
- ✅ Git 自动同步与清理脚本辅助

---

## 🔧 安装依赖

```bash
pip install -r requirements.txt
stopwatcher/
├── backtest_atr.py              # 多资产主回测脚本（整合止盈止损和历史回测）
├── simple_atr_backtest.py       # 简化版单资产回测脚本（调试用）
├── atr_strategy_backtest.py     # 全功能历史回测模块（含统计输出）
├── watcher.py                   # 实时监控止盈止损的主程序（可用于部署）
├── config.json                  # 配置文件（包含监控资产与参数）
├── summary_backtest_report.csv  # 汇总回测结果输出（自动生成）
├── AAPL_debug.csv 等            # 各资产下载的原始数据（调试用）
├── AAPL_backtest_result.csv     # 每日历史回测记录（每只股票一个文件）
├── cron_debug.log               # 定时任务调试日志
├── git_sync.sh                  # 一键 Git 提交推送脚本
├── archive_results.sh           # 清理/归档 CSV 文件的实用脚本
├── requirements.txt             # Python 依赖包列表
├── README.md                    # 项目说明文件（你正在读它）
└── venv/                        # 虚拟环境目录（已被 .gitignore 忽略）

