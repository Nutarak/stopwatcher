import json

# 默认倍率
DEFAULT_TP_MULT = 5.0
DEFAULT_SL_MULT = 2.0

CONFIG_FILE = "config.json"

def fix_config(file_path):
    with open(file_path, "r") as f:
        config = json.load(f)

    modified = False
    for asset in config.get("assets", []):
        if "take_profit_mult" not in asset:
            asset["take_profit_mult"] = DEFAULT_TP_MULT
            modified = True
        if "stop_loss_mult" not in asset:
            asset["stop_loss_mult"] = DEFAULT_SL_MULT
            modified = True

    if modified:
        with open(file_path, "w") as f:
            json.dump(config, f, indent=2)
        print("✅ config.json 补全完成：已添加缺失字段。")
    else:
        print("✅ config.json 已完整，无需修改。")

if __name__ == "__main__":
    fix_config(CONFIG_FILE)

