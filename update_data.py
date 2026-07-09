import json
from datetime import datetime
# 請保持您原本的 RAGAttributionEngine 類別定義在上方
# engine = RAGAttributionEngine() 

def generate_dashboard_data():
    # 這裡呼叫您的引擎獲取數據
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vix": "22.4",
        "rwa_flow": "+$45.8M",
        "news": [
            {
                "title": "Fed 紀要釋放 'Higher for Longer' 訊號",
                "macro": "聯準會會議紀要釋放強烈鷹派訊號，核心通膨具有黏性。",
                "spill": "台美利差維持高位，引發權值股提款壓力。",
                "recommend": [{"name": "高現金流防禦股"}],
                "risk": [{"name": "高槓桿科技股"}]
            }
            # 這裡您可以放入更多筆新聞
        ]
    }
    with open('market_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print("✅ 數據已更新至 market_data.json")

if __name__ == "__main__":
    generate_dashboard_data()
