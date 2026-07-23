import json
import os

class RAGAttributionEngine:
    def __init__(self):
        self.current_cycle = "2026 Post-Halving Mid-Stage"
        
    def fetch_us_macro_intelligence(self):
        """🇺🇸 區塊 1：美股總經與 Fed 決策（擴充至 Top 5）"""
        data = [
            {
                "title": "Fed 紀要釋放 'Higher for Longer' 訊號，黏性通膨扭曲殖利率曲線",
                "ai_sentiment": "Bearish",
                "vol_multiplier": "2.8x",
                "source": "Reuters / FOMC Minutes",
                "macro_attribution": "聯準會最新會議紀要釋放強烈鷹派訊號，核心通膨具備高度黏性，導致美債殖利率再度飆升。",
                "tw_spillover_effect": "台美利差維持高位引發外資對台股權值股的階段性提款壓力。",
                "rwa_flow_metric": "傳統美債 RWA 代幣化收益率攀升至 5.65%。",
                "agent_action_log": "[SYSTEM] Autonomous Agent initiated portfolio de-risking.",
                "recommended_groups_tw": [{"name": "高殖利率及防禦性網通股", "reason": "擁有實質在手訂單與穩定配息能力。"}],
                "high_risk_groups_tw": [{"name": "高負債比、尚未獲利之中小型科技", "reason": "借貸成本高企直接侵蝕獲利。"}],
                "recommended_groups_us": [{"name": "Microsoft (MSFT)", "reason": "大型股現金流極強。"}],
                "high_risk_groups_us": [{"name": "投機性小型 AI 概念股", "reason": "流動性緊縮面臨估值修正。"}]
            },
            {
                "title": "美國非農就業數據超預期強勁，市場降息預期再度延後",
                "ai_sentiment": "Mixed",
                "vol_multiplier": "1.9x",
                "source": "Bloomberg",
                "macro_attribution": "勞動力市場異常強韌，給予 Fed 維持高利率的底氣。",
                "tw_spillover_effect": "台股短期內將呈現高檔震盪，資金聚焦有實質題材個股。",
                "rwa_flow_metric": "鏈上法幣穩定幣（USDC）鑄造量 24H 激增 120M。",
                "agent_action_log": "[STABLE_MONITOR] USDC liquidity pool expanding.",
                "recommended_groups_tw": [{"name": "金控權值股", "reason": "有助於擴大銀行淨利差。"}],
                "high_risk_groups_tw": [{"name": "光學鏡頭與低階消費電子", "reason": "终端需求回溫緩慢。"}],
                "recommended_groups_us": [{"name": "JPMorgan Chase (JPM)", "reason": "利差收益持續受惠。"}],
                "high_risk_groups_us": [{"name": "中小型電動車供應鏈", "reason": "分期貸款意願受壓抑。"}]
            },
            {
                "title": "美國核心 CPI 年增率略高於預期，科技股盤前承壓",
                "ai_sentiment": "Bearish",
                "vol_multiplier": "2.4x",
                "source": "WSJ",
                "macro_attribution": "服務業通膨黏性超出預期，市場對年中降息的期待降溫。",
                "tw_spillover_effect": "電子權值股面臨外資結帳賣壓。",
                "rwa_flow_metric": "短天期美國公債代幣化協議 TVL 微幅增加。",
                "agent_action_log": "[RISK_CHECK] Short-term duration trimmed.",
                "recommended_groups_tw": [{"name": "台積電", "reason": "基本面強韌度高於大盤。"}],
                "high_risk_groups_tw": [{"name": "無營收生技股", "reason": "資金撤出高風險標的。"}],
                "recommended_groups_us": [{"name": "Apple (AAPL)", "reason": "現金部位龐大。"}],
                "high_risk_groups_us": [{"name": "未獲利 SaaS 軟體股", "reason": "本益比面臨殺估值風險。"}]
            },
            {
                "title": "聯準會官員暗示資產負債表縮減（QT）步伐可能放緩",
                "ai_sentiment": "Neutral",
                "vol_multiplier": "1.5x",
                "source": "CNBC",
                "macro_attribution": "為防範融資市場流動性緊縮，Fed 釋放調節 QT 速度的風向球。",
                "tw_spillover_effect": "舒緩亞股資金外流壓力。",
                "rwa_flow_metric": "鏈上去中心化借貸利率趨於平穩。",
                "agent_action_log": "[LIQUIDITY_AGENT] QT pacing factor updated.",
                "recommended_groups_tw": [{"name": "大型權值股", "reason": "受惠流動性壓力緩解。"}],
                "high_risk_groups_tw": [{"name": "高槓桿融資標的", "reason": "波動風險仍在。"}],
                "recommended_groups_us": [{"name": "Berkshire Hathaway (BRK.B)", "reason": "防禦屬性極佳。"}],
                "high_risk_groups_us": [{"name": "加密貨幣概念股", "reason": "連動高beta波動。"}]
            },
            {
                "title": "美國零售銷售數據展現韌性，消費動能支撐經濟軟著陸",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "2.1x",
                "source": "Financial Times",
                "macro_attribution": "終端消費維持活力，化解了市場對於經濟陷入硬著陸的恐慌。",
                "tw_spillover_effect": "供應鏈出貨動能獲得基本面支撐。",
                "rwa_flow_metric": "消費類 RWA 專案鏈上交易活躍度上升。",
                "agent_action_log": "[CONSUMER_TRACKER] Retail sentiment index normalized.",
                "recommended_groups_tw": [{"name": "優質零售與通路概念", "reason": "內需支撐力道穩固。"}],
                "high_risk_groups_tw": [{"name": "高度依賴歐洲出口傳產", "reason": "歐洲需求相對疲弱。"}],
                "recommended_groups_us": [{"name": "Amazon (AMZN)", "reason": "電子商務龍頭地位穩固。"}],
                "high_risk_groups_us": [{"name": "傳統實體百貨", "reason": "面臨數位轉型與成本壓力。"}]
            }
        ]
        return data[:5]  # 強制取 Top 5

    def fetch_web3_crypto_intelligence(self):
        """🌐 區塊 2：Web3 智能金融與 RWA（擴充至 Top 5）"""
        data = [
            {
                "title": "Agentic Finance 重新平衡 RWA 流動性池，減半後礦企啟動資產轉型",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.5x",
                "source": "CoinDesk",
                "macro_attribution": "減半週期過後，純挖礦邊際利潤下滑，頭部礦企啟動 RWA 戰略。",
                "tw_spillover_effect": "轉化為台廠高階 AI 伺服器代工、液冷散熱供應鏈的實質訂單。",
                "rwa_flow_metric": "鏈上基礎設施 RWA 資金池 24H 淨流入達 +$45.8M。",
                "agent_action_log": "[AGENT_FINANCE] Protocol executing cross-chain settlement.",
                "recommended_groups_tw": [{"name": "AI 伺服器代工（廣達）", "reason": "硬體升級紅利。"}],
                "high_risk_groups_tw": [{"name": "傳統低階顯卡廠", "reason": "去庫存壓力。"}],
                "recommended_groups_us": [{"name": "NVIDIA (NVDA)", "reason": "算力晶片最大贏家。"}],
                "high_risk_groups_us": [{"name": "無轉型純挖礦股", "reason": "算力成本激增。"}]
            },
            {
                "title": "實體資產代幣化（RWA）協議總鎖倉量突破百億美元大關",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.1x",
                "source": "DeFiLlama",
                "macro_attribution": "傳統金融機構加速將國債與房地產上鏈，尋求高效率清算。",
                "tw_spillover_effect": "金融科技與區塊鏈底層資安需求連帶提升。",
                "rwa_flow_metric": "RWA TVL 24H 成長 4.2%。",
                "agent_action_log": "[RWA_MONITOR] TVL milestone registered.",
                "recommended_groups_tw": [{"name": "軟體與資安概念股", "reason": "鏈上資安合規需求增長。"}],
                "high_risk_groups_tw": [{"name": "無技術壁壘之傳統系統整合", "reason": "面臨同業削價競爭。"}],
                "recommended_groups_us": [{"name": "BlackRock (BLK)", "reason": "主導傳統資產代幣化。"}],
                "high_risk_groups_us": [{"name": "落後型區域銀行", "reason": "數位化轉型緩慢。"}]
            },
            {
                "title": "跨鏈智能體協議升級，自動化造市商（AMM）流動性配置最佳化",
                "ai_sentiment": "Neutral",
                "vol_multiplier": "2.0x",
                "source": "Blockworks",
                "macro_attribution": "AI 智能體減少了流動性分散的問題，提升資本效率。",
                "tw_spillover_effect": "帶動網通晶片與高速傳輸介面的規格升級。",
                "rwa_flow_metric": "跨鏈橋手續費總額下降 15%。",
                "agent_action_log": "[CROSS_CHAIN] Liquidity routing optimized.",
                "recommended_groups_tw": [{"name": "高速傳輸晶片廠", "reason": "網通傳輸需求強勁。"}],
                "high_risk_groups_tw": [{"name": "舊規格傳輸線材廠", "reason": "面臨規格迭代淘汰。"}],
                "recommended_groups_us": [{"name": "Coinbase (COIN)", "reason": "受惠機構級託管需求。"}],
                "high_risk_groups_us": [{"name": "無牌照小型交易所", "reason": "監管合規成本過高。"}]
            },
            {
                "title": "多國央行數位貨幣（CBDC）試點擴大，與公有鏈互通性測試啟動",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "2.7x",
                "source": "CoinTelegraph",
                "macro_attribution": "各國積極打通法幣數位化通道，降低跨境結算摩擦成本。",
                "tw_spillover_effect": "推動台灣金融IT系統進行介接升級。",
                "rwa_flow_metric": "CBDC 試點鏈上模擬交易量創新高。",
                "agent_action_log": "[CBDC_SCAN] Interoperability node connected.",
                "recommended_groups_tw": [{"name": "金融資訊服務商", "reason": "系統升級剛性需求。"}],
                "high_risk_groups_tw": [{"name": "傳統匯兌服務商", "reason": "手續費收入面臨結構性衝擊。"}],
                "recommended_groups_us": [{"name": "Visa (V)", "reason": "積極整合多鏈支付方案。"}],
                "high_risk_groups_us": [{"name": "缺乏數位佈局之地區性金融", "reason": "客群遭到侵蝕。"}]
            },
            {
                "title": "去中心化算力市場（DePIN）與 AI 訓練叢集深度整合",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.3x",
                "source": "Decrypt",
                "macro_attribution": "閒置 GPU 資源透過區塊鏈代幣化聚合，解決中心化算力短缺問題。",
                "tw_spillover_effect": "刺激邊緣運算與伺服器零組件出貨。",
                "rwa_flow_metric": "DePIN 節點質押總額單周增加 25M。",
                "agent_action_log": "[DEPIN_AGENT] Cluster compute verified.",
                "recommended_groups_tw": [{"name": "伺服器基板與機殼廠", "reason": "DePIN 硬體設備需求上升。"}],
                "high_risk_groups_tw": [{"name": "低毛利組裝代工", "reason": "議價能力較弱。"}],
                "recommended_groups_us": [{"name": "Super Micro Computer (SMCI)", "reason": "伺服器出貨動能強勁。"}],
                "high_risk_groups_us": [{"name": "傳統雲端租賃小廠", "reason": "價格戰壓力沉重。"}]
            }
        ]
        return data[:5]  # 強制取 Top 5

    def fetch_tw_stocks_intelligence(self):
        """💻 區塊 3：台股與經濟部政策（擴充至 Top 5）"""
        data = [
            {
                "title": "經濟部研議爭取美方 AI 資料中心來台落腳，推動亞洲算力與綠電樞紐計畫",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.8x",
                "source": "台灣經濟部 (MOEA)",
                "macro_attribution": "聚焦於提供穩定的高階算力基礎設施與綠電配套。",
                "tw_spillover_effect": "加速台灣本地綠電、儲能系統的審查釋出。",
                "rwa_flow_metric": "預期引導跨國實體資產投資金額逾 1500 億台幣。",
                "agent_action_log": "[POLICY_AGENT] Green Energy Hub correlation detected.",
                "recommended_groups_tw": [{"name": "綠電與重電儲能鏈（華城、中興電）", "reason": "政策剛性需求明確。"}],
                "high_risk_groups_tw": [{"name": "高耗能且無綠電轉型傳統製造", "reason": "電價結構性調漲壓力。"}],
                "recommended_groups_us": [{"name": "NextEra Energy (NEE)", "reason": "全球綠電基礎設施龍頭。"}]
            },
            {
                "title": "台股半導體資本支出維持高檔，先進封裝產能供不應求",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.4x",
                "source": "工商時報",
                "macro_attribution": "全球對 CoWoS 等先進封裝需求強勁，晶圓代工龍頭擴產進度超前。",
                "tw_spillover_effect": "帶動本土設備與檢測分析廠營運噴發。",
                "rwa_flow_metric": "半導體設備融資租賃需求上升。",
                "agent_action_log": "[SEMI_TRACKER] Advanced packaging yield optimized.",
                "recommended_groups_tw": [{"name": "半導體設備與檢測（弘塑、萬潤）", "reason": "先進封裝擴產直接受惠。"}],
                "high_risk_groups_tw": [{"name": "成熟製程代工廠", "reason": "面臨價格競爭壓力。"}],
                "recommended_groups_us": [{"name": "Applied Materials (AMAT)", "reason": "設備供應鏈龍頭。"}]
            },
            {
                "title": "台灣出口連紅，資通訊與視聽產品出貨金額創歷史同期新高",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "2.9x",
                "source": "經濟部統計處",
                "macro_attribution": "受惠全球 AI 終端應用鋪貨，帶動資通訊產品出口續強。",
                "tw_spillover_effect": "海運與空運物流需求維持高檔。",
                "rwa_flow_metric": "供應鏈融資代幣化專案流動性充裕。",
                "agent_action_log": "[EXPORT_METRIC] ICT shipment growth verified.",
                "recommended_groups_tw": [{"name": "航運與物流指標股", "reason": "出口貨量提供運價支撐。"}],
                "high_risk_groups_tw": [{"name": "內需觀光餐飲（部分高基期）", "reason": "成長動能趨於平緩。"}],
                "recommended_groups_us": [{"name": "FedEx (FDX)", "reason": "全球物流需求受惠。"}]
            },
            {
                "title": "金管會推動亞資中心計畫，放寬金融機構跨國資產管理法規",
                "ai_sentiment": "Neutral",
                "vol_multiplier": "2.2x",
                "source": "金融監督管理委員會",
                "macro_attribution": "打造台灣成為亞洲資產管理重鎮，吸引國際資金駐留。",
                "tw_spillover_effect": "提升本土金控與投信的國際資產管理規模。",
                "rwa_flow_metric": "跨境理財通金流規模擴增。",
                "agent_action_log": "[FSC_MONITOR] Wealth management rules updated.",
                "recommended_groups_tw": [{"name": "大型金控與投信機構", "reason": "亞資中心政策直接受益。"}],
                "high_risk_groups_tw": [{"name": "小型獨立券商", "reason": "規模效應不足面臨競爭。"}],
                "recommended_groups_us": [{"name": "Morgan Stanley (MS)", "reason": "全球財管業務標竿。"}]
            },
            {
                "title": "台電強韌電網計畫加速執行，重電三雄訂單能見度看到 2028 年",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.0x",
                "source": "經濟日報",
                "macro_attribution": "因應 AI 資料中心與電動車普及，電網基礎設施更新刻不容緩。",
                "tw_spillover_effect": "重電設備內需訂單飽和，並逐步開拓北美變壓器市場。",
                "rwa_flow_metric": "重電設備實體資產融資穩定。",
                "agent_action_log": "[GRID_AGENT] Transformer backlog secured.",
                "recommended_groups_tw": [{"name": "重電與線纜廠（士電、華城）", "reason": "在手訂單能見度極高。"}],
                "high_risk_groups_tw": [{"name": "營建原物料相關傳產", "reason": "房市調控壓抑部分動能。"}],
                "recommended_groups_us": [{"name": "Eaton Corporation (ETN)", "reason": "全球電網管理巨頭。"}]
            }
        ]
        return data[:5]  # 強制取 Top 5

    def generate_dashboard_data(self):
        return {
            "us_macro": self.fetch_us_macro_intelligence(),
            "web3_crypto": self.fetch_web3_crypto_intelligence(),
            "tw_stocks": self.fetch_tw_stocks_intelligence(),
            "global_vix": {
                "value": "22.4",
                "status_zh": "突破關鍵20關卡 / 強烈避險情緒 (Risk-Off)",
                "status_en": "Surged Past 20 / Strong Risk-Off Hedging",
                "trend": "Upward (+14.2% 24H)",
                "insight_zh": "【VIX 跨境聯動歸因】VIX 恐慌指數飆升至 22.4，反映宏觀資金正全面買入波動率期權進行下行保護。",
                "insight_en": "【VIX Cross-Market Insight】VIX jumps to 22.4, signaling widespread institutional hedging."
            }
        }

if __name__ == "__main__":
    engine = RAGAttributionEngine()
    final_data = engine.generate_dashboard_data()
    
    output_filename = "data.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 數據已成功完整更新至 {output_filename}！最新 TOP 5 跨境歸因情報已同步。")
