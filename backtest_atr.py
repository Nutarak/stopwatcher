import json
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

# === 参数 ===
MAX_LOOKBACK_DAYS = 10
HOLD_DAYS = 10  # 最大持仓观察日数
start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")

# === 配置读取 ===
with open("config.json", "r") as f:
    config = json.load(f)

# === 获取数据 ===
def get_data(symbol: str, start_date: str) -> pd.DataFrame:
    try:
        df = yf.Ticker(symbol).history(start=start_date)
        df.columns = [c.lower() for c in df.columns]
        df["atr_14"] = ta.atr(high=df["high"], low=df["low"], close=df["close"], length=14)
        df.to_csv(f"{symbol}_debug.csv")
        return df
    except Exception as e:
        print(f"❌ 获取 {symbol} 数据失败：{e}")
        return pd.DataFrame()

# === 回测函数 ===
def backtest_asset(symbol: str, tp_mult: float, sl_mult: float) -> dict:
    print(f"\n📈 回测 {symbol}（TP×{tp_mult}, SL×{sl_mult}）")
    df = get_data(symbol, start_date)
    if df.empty or df["atr_14"].isna().all():
        print(f"⚠️ {symbol} 无有效数据")
        return {"symbol": symbol, "tp": "-", "sl": "-", "tp_count": 0, "sl_count": 0, "hold": 0, "total": 0, "winrate": "-"}

    # 当前止盈止损估算
    latest = df.iloc[-1]
    price_now = latest["close"]
    atr_now = latest["atr_14"]
    tp_now = price_now * (1 + atr_now * tp_mult / price_now)
    sl_now = price_now * (1 - atr_now * sl_mult / price_now)
    print(f"📌 当前价格 {price_now:.2f}, ATR {atr_now:.2f} → TP {tp_now:.2f}, SL {sl_now:.2f}")

    # 历史回测
    results = []
    for i in range(len(df) - HOLD_DAYS):
        row = df.iloc[i]
        price = row["close"]
        atr = row["atr_14"]
        if pd.isna(price) or pd.isna(atr):
            continue
        tp = price * (1 + atr * tp_mult / price)
        sl = price * (1 - atr * sl_mult / price)

        result = "HOLD"
        for j in range(1, HOLD_DAYS + 1):
            future = df.iloc[i + j]
            if pd.isna(future["high"]) or pd.isna(future["low"]):
                continue
            if future["high"] >= tp:
                result = "TP"
                break
            if future["low"] <= sl:
                result = "SL"
                break

        results.append({
            "date": df.index[i].strftime("%Y-%m-%d"),
            "price": price,
            "atr": atr,
            "tp": tp,
            "sl": sl,
            "result": result
        })

    df_result = pd.DataFrame(results)
    df_result.to_csv(f"{symbol}_backtest_result.csv", index=False)
    tp_count = (df_result["result"] == "TP").sum()
    sl_count = (df_result["result"] == "SL").sum()
    hold_count = (df_result["result"] == "HOLD").sum()
    total = len(df_result)
    winrate = f"{(tp_count / (tp_count + sl_count) * 100):.2f}%" if (tp_count + sl_count) > 0 else "-"

    print(f"✅ 回测完成：共 {total} 天 | TP: {tp_count} | SL: {sl_count} | HOLD: {hold_count} | 胜率: {winrate}")
    return {
        "symbol": symbol,
        "tp": f"{tp_now:.2f}",
        "sl": f"{sl_now:.2f}",
        "tp_count": tp_count,
        "sl_count": sl_count,
        "hold": hold_count,
        "total": total,
        "winrate": winrate
    }

# === 主程序 ===
def main():
    print("📊 多资产 ATR 策略历史回测 + 当前止盈止损建议\n")
    summary = []

    for asset in config["assets"]:
        result = backtest_asset(asset["symbol"], asset["take_profit_mult"], asset["stop_loss_mult"])
        summary.append(result)

    df_summary = pd.DataFrame(summary)
    df_summary.to_csv("summary_backtest_report.csv", index=False)
    print("\n📄 总结报告已保存为 summary_backtest_report.csv")

if __name__ == "__main__":
    main()

