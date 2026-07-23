import json
import random
from datetime import datetime

# ==========================================
# ⚙️ 系統設定與權重參數 (Hyperparameters)
# ==========================================
W_NLP = 0.6       # 輿情 NLP 看多/看空權重
W_VIX = 0.4       # VIX 恐慌情緒減項權重

# ==========================================
# 1️⃣ [階段一] 輿情與總經數據採集模組 (Ingestion & Sentiment)
# ==========================================
def fetch_macro_and_sentiment_sources():
    """
    模擬/採集來自 Bloomberg, CoinDesk, X(Twitter) 與 Fed 官網之輿情流
    """
    raw_feeds = [
        # 美股與總經消息 (US Macro)
        {
            "category": "us_macro",
            "source": "Bloomberg / Fed RSS",
            "title": "聯準會釋出降息訊號，美債殖利率曲線持續平坦化",
            "raw_text": "Fed 官員最新言論顯示通脹趨勢符合預期，市場對降息預期升溫，長天期美債吸引避險與鎖利資金流入。",
            "nlp_score": 0.75, # 0.0 (極度悲觀) ~ 1.0 (極度樂觀)
            "vix_impact": 0.2
        },
        {
            "category": "us_macro",
            "source": "Wall Street Journal",
            "title": "大型科技股資本支出 (CapEx) 激增，邊緣 AI 計算需求強勁",
            "raw_text": "雲端巨頭持續擴大資料中心與邊緣 AI 伺服器投資，激發半導體與電力設備類股上漲動能。",
            "nlp_score": 0.82,
            "vix_impact": 0.1
        },

        # Web3 與 RWA 智能金融消息 (Web3 Crypto & RWA)
        {
            "category": "web3_crypto",
            "source": "CoinDesk / On-Chain Analytics",
            "title": "機構級美國國債 RWA 代幣化規模突破歷史新高，Agentic AI 流動性池爆發",
            "raw_text": "傳統機構將短期國債加速帶入鏈上，結合自主 AI Agent 執行套利與流動性再平衡，帶動鏈上資產淨流入。",
            "nlp_score": 0.88,
            "vix_impact": -0.1
        },
        {
            "category": "web3_crypto",
            "source": "X (Twitter) KOL Signal",
            "title": "去中心化邊緣 AI 算力網絡費用收益率提升，質押率顯著上升",
            "raw_text": "鏈上數據顯示分散式算力協議的算力利用率達 85%，帶動基礎設施代幣資金持續淨流入。",
            "nlp_score": 0.70,
            "vix_impact": 0.0
        },

        # 台股與產業政策消息 (Taiwan Stocks & Policy)
        {
            "category": "tw_stocks",
            "source": "經濟日報 / 經濟部政策新聞",
            "title": "經濟部推動先進封裝與邊緣 AI 產業供應鏈，台廠迎急單潮",
            "raw_text": "台積電 2 奈米進展順利，先進封裝 (CoWoS) 產能持續供不應求，帶動相關設備與伺服器組裝廠營收衝高。",
            "nlp_score": 0.85,
            "vix_impact": 0.1
        }
    ]
    
    # 模擬當前全球 VIX 恐慌指數 (當 > 20 時啟動避險 alert)
    vix_data = {
        "value": 22.4,
        "status_zh": "突破關鍵20關卡 / 強烈避險情緒 (Risk-Off)",
        "status_en": "Surpassed Key 20 Level / Strong Risk-Off",
        "insight_zh": "⚠️ 當前 VIX 突破 20 關鍵關卡 (22.4)，市場避險情緒 (Risk-Off) 顯著升溫。建議提高美債 RWA 代幣與防禦型高殖利率資產比重，適度降低高 Beta 股票槓桿。",
        "insight_en": "⚠️ VIX has crossed the key 20 benchmark (22.4), indicating heightened Risk-Off sentiment. Increase allocations in Treasury RWAs and high-dividend assets while reducing high-Beta stock leverage."
    }
    
    return raw_feeds, vix_data


# ==========================================
# 2️⃣ [階段二] Agentic 推薦推理矩陣 (Agentic Decision Matrix)
# ==========================================
class AgenticRecommendationEngine:
    """
    AI Agent 推理引擎：根據 [總經 Macro + 輿情 Sentiment + VIX 風險] 輸出資產建議
    """
    
    @staticmethod
    def evaluate_composite_sentiment(nlp_score, vix_value):
        """ 計算綜合情緒分數與評級 """
        # 將 VIX (10~40) 標準化為 0~1 的風險係數
        vix_normalized = min(max((vix_value - 10) / 30.0, 0.0), 1.0)
        
        # 綜合分數 = NLP 看多分數 - VIX 恐慌扣分
        composite_score = (W_NLP * nlp_score) - (W_VIX * vix_normalized * 0.5)
        
        if composite_score >= 0.55:
            sentiment_tag = "Bullish"
        elif composite_score <= 0.35:
            sentiment_tag = "Bearish"
        else:
            sentiment_tag = "Neutral"
            
        vol_multiplier = f"{round(1.0 + (vix_value / 50.0), 1)}x"
        return sentiment_tag, vol_multiplier, composite_score

    @staticmethod
    def generate_recommendations(category, sentiment_tag, vix_value):
        """
        Agentic 推理邏輯：根據市場狀態產出具體推薦與風險警示標的
        """
        is_high_risk_env = vix_value > 20.0
        
        if category == "us_macro":
            rec_us = [
                {"name": "TLT / iShares 20+ 年美債 ETF", "reason": "降息預期升溫，長天期公債鎖利與避險價值凸顯"},
                {"name": "NVDA / MSFT (AI 巨頭)", "reason": "資本支出強勁，邊緣 AI 算力需求帶來業績支撐"}
            ]
            risk_us = [
                {"name": "高負債小型成長股 (IWM)", "reason": "高利率尾端壓力仍存，避險情緒下資金偏好大型藍籌"}
            ] if is_high_risk_env else []
            
            rec_tw, risk_tw = [], []

        elif category == "web3_crypto":
            rec_us = []
            risk_us = []
            rec_tw = [
                {"name": "鏈上美債 RWA 代幣 (O Ondo / BUIDL)", "reason": "無風險利率轉化，Risk-Off 環境下首選無損避險收益"},
                {"name": "Agentic AI 算力基礎設施代幣", "reason": "邊緣 AI 計算網路代幣化帶動真實協議費用收益"}
            ]
            risk_tw = [
                {"name": "無資產背書之高槓桿迷因幣", "reason": "VIX 突破 20 時流動性快速收縮，高風險資產面臨回檔"}
            ] if is_high_risk_env else []

        else: # tw_stocks
            rec_tw = [
                {"name": "台積電 (2330) / 鴻海 (2317)", "reason": "先進封裝產能滿載，AI 伺服器組裝出口動能強勁"},
                {"name": "緯創 (3231) / 廣達 (2382)", "reason": "邊緣 AI 伺服器與水冷散熱解決方案需求明確"}
            ]
            risk_tw = [
                {"name": "高估值無獲利支撐之概念股", "reason": "大盤隨 VIX 波動加大，資金加速退潮回歸績優權值股"}
            ] if is_high_risk_env else []
            
            rec_us, risk_us = [], []

        return rec_tw, risk_tw, rec_us, risk_us


# ==========================================
# 3️⃣ RAG 管道執行與 JSON 生成器
# ==========================================
def run_rag_pipeline():
    print("🚀 [Step 1/3] 正在採集總經數據、新聞輿情與 VIX 恐慌指數...")
    raw_feeds, vix_data = fetch_macro_and_sentiment_sources()
    
    output_data = {
        "global_vix": vix_data,
        "us_macro": [],
        "web3_crypto": [],
        "tw_stocks": []
    }
    
    engine = AgenticRecommendationEngine()
    print("🤖 [Step 2/3] 正在執行 Agentic 推理矩陣 (Macro + Sentiment + Profiling)...")

    for feed in raw_feeds:
        category = feed["category"]
        nlp_score = feed["nlp_score"]
        
        # 計算綜合情緒與波動倍率
        sentiment_tag, vol_mult, composite_score = engine.evaluate_composite_sentiment(
            nlp_score, vix_data["value"]
        )
        
        # Agentic 推薦推理
        rec_tw, risk_tw, rec_us, risk_us = engine.generate_recommendations(
            category, sentiment_tag, vix_data["value"]
        )
        
        # 建立格式符合 index.html 的新聞卡片資料結構
        news_item = {
            "title": feed["title"],
            "ai_sentiment": sentiment_tag,
            "vol_multiplier": vol_mult,
            "source": feed["source"],
            "macro_attribution": f"{feed['raw_text']} (綜合情緒指數: {round(composite_score, 2)})",
            "tw_spillover_effect": f"連動影響：帶動資金轉向具備真實收益 (Real Yield) 與政策加持之標的。",
            "rwa_flow_metric": "+$52.4M Pool Inflow (Agentic AI Net Allocation)",
            "agent_action_log": f"[AGENT EXEC] Rebalanced risk exposure based on VIX {vix_data['value']}.",
            "recommended_groups_tw": rec_tw,
            "high_risk_groups_tw": risk_tw,
            "recommended_groups_us": rec_us,
            "high_risk_groups_us": risk_us
        }
        
        output_data[category].append(news_item)

    # 寫入 data.json
    print("💾 [Step 3/3] 正在將分析結果寫入 data.json...")
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print("✨ [成功] data.json 更新完成！請重新整理 index.html 查看最新動態看板。")

if __name__ == "__main__":
    run_rag_pipeline()
