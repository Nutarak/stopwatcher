import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

# ===== 配置 =====
symbol = "AAPL"
take_profit_mult = 4.0
stop_loss_mult = 2.0
start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

# ===== 下载数据 =====
print(f"> 正在下载 {symbol} 数据...")
try:
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date)
    if df.empty:
        raise ValueError("数据为空，可能是网络问题或无交易数据")

    df.columns = [c.lower() for c in df.columns]
    df.to_csv(f"{symbol}_debug.csv")
    print(f"> 下载成功，共 {len(df)} 行，列名：{df.columns.tolist()}")

except Exception as e:
    print(f"[错误] 无法下载数据：{e}")
    exit(1)

# ===== 检查必要列 =====
required_cols = {"high", "low", "close"}
if not required_cols.issubset(df.columns):
    print(f"[错误] 缺少列：{required_cols - set(df.columns)}")
    exit(1)

# ===== 计算 ATR =====
print("> 正在计算 ATR...")
df["atr_14"] = ta.atr(high=df["high"], low=df["low"], close=df["close"], length=14)

if df["atr_14"].isna().all():
    print("[错误] ATR 计算失败，结果全为 NaN")
    exit(1)

# ===== 回测计算 =====
latest = df.iloc[-1]
price = latest["close"]
atr = latest["atr_14"]

if pd.isna(price) or pd.isna(atr):
    print("[错误] 收盘价或 ATR 值无效")
    exit(1)

tp = price * (1 + atr * take_profit_mult / price)
sl = price * (1 - atr * stop_loss_mult / price)
trigger_date = df.index[-1].strftime("%Y-%m-%d")
return_pct = (tp / price - 1) * 100

# ===== 输出结果 =====
print(f"\n✅ {symbol} 回测完成：")
print(f"- 触发日：{trigger_date}")
print(f"- 当前价格：{price:.2f}")
print(f"- ATR：{atr:.2f}")
print(f"- 止盈价：{tp:.2f}")
print(f"- 止损价：{sl:.2f}")
print(f"- 预期收益率：{return_pct:.2f}%")

