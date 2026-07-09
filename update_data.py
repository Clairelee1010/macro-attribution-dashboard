import json
import os

class RAGAttributionEngine:
    def __init__(self):
        self.current_cycle = "2026 Post-Halving Mid-Stage"
        
    def fetch_us_macro_intelligence(self):
        # 配合前端，將 Key 值精準對齊 index.html 的欄位名稱
        return [
            {
                "title_zh": "Fed 紀要釋放 'Higher for Longer' 訊號，黏性通膨扭曲殖利率曲線",
                "macro_attribution_zh": "【美股總經大腦】聯準會會議紀要釋放強烈鷹派訊號，核心通膨（PCE）具黏性導致美債殖利率再度飆升。傳統科技股面臨估值修正，迫使跨市場資金從投機性高槓桿資產撤出，轉向具備實質基本面與強大現金流的防禦性標的。",
                "risk_attribution_zh": "【風險提示】高負債比、依賴低息貸款的中小型科技股基本面將面臨週轉壓力測試。建議配置：Microsoft (MSFT)、NextEra Energy (NEE) 等大型防禦性現金流標的。"
            },
            {
                "title_zh": "美債殖利率曲線持續倒掛，市場流動性面臨洗盤",
                "macro_attribution_zh": "長短債利差持續收斂，反映市場對中長期經濟增長放緩的擔憂。鏈上 RWA 資產配置顯示避險資金大規模湧入代幣化美債池。",
                "risk_attribution_zh": "【避險觀測】建議關注台股高殖利率及強大現金流之防禦性網通股；避開高本益比、尚未獲利的投機題材。"
            }
        ]

    def generate_dashboard_data(self):
        return {
            "us_macro": self.fetch_us_macro_intelligence()
        }

if __name__ == "__main__":
    engine = RAGAttributionEngine()
    final_data = engine.generate_dashboard_data()
    
    # 強制指定輸出檔名為 dashboard_data.json，完美對接前端第 19 行的 fetch
    output_filename = 'dashboard_data.json'
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 數據已成功更新至 {output_filename}！欄位名稱已完美對其 _zh 後綴。")
