import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

with open("config.json", "r") as f:
    config = json.load(f)

start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")

print("🔍 开始验证 symbol 是否有效...\n")

for asset in config["assets"]:
    symbol = asset.get("symbol")
    print(f"⏳ 正在检查 {symbol}...")
    try:
        df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False, progress=False)

        # 处理列名：确保无 MultiIndex 且大小写统一
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns = [str(col).title() for col in df.columns]

        required_cols = {"High", "Low", "Close"}
        if df.empty:
            print(f"❌ {symbol} 无数据（可能代码错误或停牌）")
        elif not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            print(f"⚠️ {symbol} 数据不完整，缺少列: {missing}")
        else:
            print(f"✅ {symbol} 数据可用，共 {len(df)} 日记录")
    except Exception as e:
        print(f"❌ {symbol} 下载异常：{e}")

print("\n📋 检查完成。")

