import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

# ===== 策略参数 =====
symbol = "AAPL"
tp_mult = 4.0
sl_mult = 2.0
holding_days = 10  # 最大持有天数
start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

# ===== 下载数据 =====
print(f"> 下载 {symbol} 数据...")
df = yf.Ticker(symbol).history(start=start_date)
df.columns = [c.lower() for c in df.columns]

# ===== 计算 ATR =====
df["atr_14"] = ta.atr(high=df["high"], low=df["low"], close=df["close"], length=14)

# ===== 回测逻辑 =====
results = []
for i in range(len(df) - holding_days):
    row = df.iloc[i]
    price = row["close"]
    atr = row["atr_14"]
    if pd.isna(price) or pd.isna(atr):
        continue

    tp = price * (1 + atr * tp_mult / price)
    sl = price * (1 - atr * sl_mult / price)

    triggered = None
    for j in range(1, holding_days + 1):
        future = df.iloc[i + j]
        high = future["high"]
        low = future["low"]

        if pd.isna(high) or pd.isna(low):
            continue

        if high >= tp:
            triggered = "TP"
            break
        if low <= sl:
            triggered = "SL"
            break

    results.append({
        "date": df.index[i].strftime("%Y-%m-%d"),
        "price": price,
        "atr": atr,
        "tp": tp,
        "sl": sl,
        "result": triggered or "HOLD"
    })

# ===== 汇总统计 =====
df_result = pd.DataFrame(results)
total = len(df_result)
tp_count = (df_result["result"] == "TP").sum()
sl_count = (df_result["result"] == "SL").sum()
hold_count = (df_result["result"] == "HOLD").sum()

print("\n✅ 回测完成：")
print(f"- 总交易日：{total}")
print(f"- 止盈次数：{tp_count}")
print(f"- 止损次数：{sl_count}")
print(f"- 持仓未触发：{hold_count}")
print(f"- 胜率（TP / 有触发）：{tp_count / (tp_count + sl_count) * 100:.2f}%" if (tp_count + sl_count) > 0 else "- 无触发数据")

# ===== 保存结果表格 =====
df_result.to_csv(f"{symbol}_backtest_result.csv", index=False)
print(f"\n📄 明细已保存至 {symbol}_backtest_result.csv")

