import json

# 1. 確保引擎定義是完整的 (直接重新定義整合後的 Class)
class RAGAttributionEngine:
    def __init__(self):
        self.current_cycle = "2026 Post-Halving Mid-Stage"
    
    # 這裡放我們剛剛確認過沒問題的函式
    def fetch_us_macro_intelligence(self):
        return [{"title_zh": "Fed 紀要釋放 'Higher for Longer' 訊號，黏性通膨扭曲殖利率曲線", "title_en": "Fed Minutes Signal 'Higher for Longer' as Sticky Inflation Distorts Yield Curve", "source": "Reuters / FOMC Minutes", "ai_sentiment": "Bearish", "vol_multiplier": "2.8x", "url": "https://www.reuters.com", "macro_attribution_zh": "聯準會會議紀要釋放強烈鷹派訊號"}]
    
    def fetch_web3_crypto_intelligence(self):
        return [{"title_zh": "Web3 資金流動正常", "ai_sentiment": "Neutral"}] # 簡化測試
    
    def fetch_tw_stocks_intelligence(self):
        return [{"title_zh": "台股經濟部快訊", "ai_sentiment": "Stable"}] # 簡化測試

    def generate_dashboard_data(self):
        data = {
            "us_macro": self.fetch_us_macro_intelligence(),
            "web3_crypto": self.fetch_web3_crypto_intelligence(),
            "tw_stocks": self.fetch_tw_stocks_intelligence()
        }
        return data

# 2. 執行產生資料
engine = RAGAttributionEngine()
final_data = engine.generate_dashboard_data()

# 3. 寫入檔案
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print("成功！data.json 已經產生，請到左側檔案區下載。")
