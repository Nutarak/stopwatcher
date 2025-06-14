import yfinance as yf
import pandas_ta as ta

# 设置测试股票与周期
symbol = "TSLA"
period = "14d"
interval = "1d"

print(f"⏳ 正在获取 {symbol} 最近 {period} 的数据...")

# 下载历史数据
df = yf.download(symbol, period=period, interval=interval)

# 检查数据是否加载成功
if df.empty:
    print("❌ 获取失败，数据为空")
else:
    # 计算 ATR（14日）
    df["ATR"] = ta.atr(high=df["High"], low=df["Low"], close=df["Close"], length=14)

    # 显示结果
    print("📊 ATR 计算结果（最新）:")
    print(df[["Close", "ATR"]].tail())

