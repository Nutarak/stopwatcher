import os
import json
import yfinance as yf
import requests
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from dotenv import load_dotenv

# === 加载 .env 配置 ===
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

# === Telegram 推送函数 ===
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_USER_ID, "text": text}
    try:
        response = requests.post(url, data=data)
        print(f"[Telegram] 状态码: {response.status_code}")
    except Exception as e:
        print(f"[Telegram] 推送失败: {e}")

# === 状态文件读写 ===
def load_state():
    try:
        with open("state.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f)

# === 加载配置文件 ===
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

# === 主判断逻辑 ===
def check_prices(assets):
    print(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    state = load_state()

    for asset in assets:
        if not asset.get("active", True):
            continue

        symbol = asset["symbol"]
        buy_price = asset["buy_price"]
        sl_mult = asset.get("atr_stop_loss_multiplier", 2.0)
        tp_mult = asset.get("atr_take_profit_multiplier", 3.0)

        print(f"🔍 {symbol}: 获取价格中...")

        data = yf.Ticker(symbol).history(period="2d", interval="5m")

        if data.empty or len(data) < 20:
            print(f"{symbol}: ❌ 数据不足")
            continue

        data["ATR"] = ta.atr(high=data["High"], low=data["Low"], close=data["Close"], length=14)
        atr = data["ATR"].iloc[-1]
        price = data["Close"].iloc[-1]

        if pd.isna(atr):
            print(f"{symbol}: ❌ 无法计算 ATR")
            continue

        tp_price = buy_price + tp_mult * atr
        sl_price = buy_price - sl_mult * atr

        print(f"{symbol} 当前价格: {price:.2f} | ATR: {atr:.2f} | 止盈: {tp_price:.2f} | 止损: {sl_price:.2f}")

        # 检查是否已提醒
        if symbol in state and state[symbol] in ["tp", "sl"]:
            continue

        if price >= tp_price:
            msg = f"✅ {symbol} 当前价格 {price:.2f} 已触发止盈（目标: {tp_price:.2f}）"
            print(msg)
            send_telegram_message(msg)
            state[symbol] = "tp"
        elif price <= sl_price:
            msg = f"⚠️ {symbol} 当前价格 {price:.2f} 已触发止损（目标: {sl_price:.2f}）"
            print(msg)
            send_telegram_message(msg)
            state[symbol] = "sl"

    save_state(state)

# === 主入口 ===
if __name__ == "__main__":
    config = load_config()
    check_prices(config["assets"])

