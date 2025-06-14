import os
import json
import yfinance as yf
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


# === Telegram 通知设定 ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")


# 状态保存文件路径
STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_USER_ID,
        "text": text
    }
    print(f"[调试] 正在尝试发送 Telegram 消息: {text}")
    try:
        response = requests.post(url, data=data)
        print(f"[调试] Telegram API 响应状态码: {response.status_code}")
        print(f"[调试] 返回内容: {response.text}")
    except Exception as e:
        print(f"Telegram 通知失败: {e}")

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as f:
        return json.load(f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def check_prices(assets):
    print(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    state = load_state()

    for asset in assets:
        if not asset.get("active", True):
            continue

        symbol = asset["symbol"]
        buy_price = asset["buy_price"]
        tp_pct = asset["take_profit_pct"]
        sl_pct = asset["stop_loss_pct"]

        data = yf.Ticker(symbol).history(period="1d", interval="5m")
        if data.empty:
            print(f"{symbol}: ❌ 无法获取价格数据")
            continue

        current_price = data["Close"].iloc[-1]
        tp_price = buy_price * (1 + tp_pct)
        sl_price = buy_price * (1 - sl_pct)

        print(f"{symbol} 当前价格: {current_price:.2f} | 止盈: {tp_price:.2f} | 止损: {sl_price:.2f}")

        already_triggered = state.get(symbol)

        if current_price >= tp_price and already_triggered != "tp":
            message = f"✅ {symbol} 当前价格 {current_price:.2f} 已触发止盈（目标: {tp_price:.2f}）"
            print(message)
            send_telegram_message(message)
            state[symbol] = "tp"

        elif current_price <= sl_price and already_triggered != "sl":
            message = f"⚠️ {symbol} 当前价格 {current_price:.2f} 已触发止损（目标: {sl_price:.2f}）"
            print(message)
            send_telegram_message(message)
            state[symbol] = "sl"

    save_state(state)

if __name__ == "__main__":
    config = load_config()
    check_prices(config["assets"])

