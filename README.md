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

