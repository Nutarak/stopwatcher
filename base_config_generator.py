import json

# 配置列表：股票代码、买入价、止盈倍率、止损倍率
assets = [
    {"symbol": "TSLA", "buy_price": 250.0, "take_profit_mult": 5.0, "stop_loss_mult": 2.0},
    {"symbol": "NVDA", "buy_price": 1100.0, "take_profit_mult": 6.0, "stop_loss_mult": 3.0},
    {"symbol": "AMD", "buy_price": 155.0, "take_profit_mult": 5.5, "stop_loss_mult": 2.5},
    {"symbol": "PLTR", "buy_price": 22.0, "take_profit_mult": 4.0, "stop_loss_mult": 2.0},
    {"symbol": "BNTX", "buy_price": 95.0, "take_profit_mult": 5.0, "stop_loss_mult": 2.0},
]

# 构造最终 config.json 格式
config_data = {
    "assets": [
        {
            "symbol": asset["symbol"],
            "buy_price": asset["buy_price"],
            "take_profit_mult": asset["take_profit_mult"],
            "stop_loss_mult": asset["stop_loss_mult"],
            "active": True
        }
        for asset in assets
    ]
}

# 写入 config.json
with open("config.json", "w") as f:
    json.dump(config_data, f, indent=2)

print("✅ 已生成 config.json（含倍率参数）")

