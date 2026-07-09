# 這是您 Python 腳本的結尾部分，請將其替換為這段：
import json

# 假設 engine 是您定義好的類別
data_to_save = {
    "us_macro": engine.fetch_us_macro_intelligence(),
    "web3_rwa": engine.fetch_web3_rwa_intelligence(),
    "tw_market": engine.fetch_tw_market_intelligence()
}

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_to_save, f, ensure_ascii=False)

print("🎯 數據已更新！請開啟您的 index.html 查看最新看板。")
