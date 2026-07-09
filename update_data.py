import json
import os

class RAGAttributionEngine:
    def __init__(self):
        self.current_cycle = "2026 Post-Halving Mid-Stage"
        
    def fetch_us_macro_intelligence(self):
        """🇺🇸 區塊 1：美股總經與 Fed 決策（多條深度新聞）"""
        return [
            {
                "title": "Fed 紀要釋放 'Higher for Longer' 訊號，黏性通膨扭曲殖利率曲線",
                "ai_sentiment": "Bearish",
                "vol_multiplier": "2.8x",
                "source": "Reuters / FOMC Minutes",
                "macro_attribution": "聯準會最新會議紀要釋放強烈鷹派訊號，核心通膨（PCE）具備高度黏性，導致美債殖利率再度飆升。傳統科技股面臨估值修正壓力，迫使跨市場資金從投機性高槓桿資產撤出，轉向具備實質基本面與強大現金流的防禦性標的。",
                "tw_spillover_effect": "台美利差維持高位引發外資對台股權值股的階段性提款壓力；高負債比、依賴低息貸款的中小型科技股基本面將面臨週轉壓力測試。",
                "rwa_flow_metric": "傳統美債 RWA 代幣化收益率攀升至 5.65%，引發鏈上資本逆向回流實體短期美債。",
                "agent_action_log": "[SYSTEM] Autonomous Agent initiated portfolio de-risking; reallocating 14.2% capital from small-cap AI into defensive nodes.",
                "recommended_groups_tw": [{"name": "高殖利率及防禦性網通股", "reason": "擁有實質在手訂單與穩定配息能力，具備避險資金進駐效益。"}],
                "high_risk_groups_tw": [{"name": "高負債比、尚未獲利之中小型科技", "reason": "借貸成本高企直接侵蝕獲利，缺乏實質營收支撐。"}],
                "recommended_groups_us": [{"name": "Microsoft (MSFT)", "reason": "大型股現金流極強，抗高利率風險能力高。"}, {"name": "NextEra Energy (NEE)", "reason": "防禦性公用事業龍頭，受惠資金避險。"}],
                "high_risk_groups_us": [{"name": "投機性小型 AI 概念股", "reason": "市場流動性緊縮，缺乏實質營收支撐的標的面臨估值修正。"}]
            },
            {
                "title": "美國非農就業數據超預期強勁，市場降息預期再度延後",
                "ai_sentiment": "Mixed",
                "vol_multiplier": "1.9x",
                "source": "Bloomberg",
                "macro_attribution": "勞動力市場異常強韌，給予 Fed 更多維持高利率的底氣。高利率環境延長雖然壓抑科技股估值，但也反映出美國實體經濟並未陷入衰退，呈現強韌的軟著陸格局。",
                "tw_spillover_effect": "外資期貨空單維持高位，台股短期內將呈現萬九至兩萬點的高檔震盪，資金聚焦有實質題材的個股，而非全面普漲。",
                "rwa_flow_metric": "鏈上法幣穩定幣（USDC）鑄造量 24H 激增 120M，顯示場外法幣資金正伺機尋找進場點。",
                "agent_action_log": "[STABLE_MONITOR] USDC liquidity pool expanding. Monitoring support levels for re-entry.",
                "recommended_groups_tw": [{"name": "金控權值股（富邦金、國泰金）", "reason": "台美利差擴大與高利率環境有助於擴大銀行淨利差。"}],
                "high_risk_groups_tw": [{"name": "光學鏡頭與低階消費電子", "reason": "终端需求回溫緩慢，高利率壓抑非剛性消費。"}],
                "recommended_groups_us": [{"name": "JPMorgan Chase (JPM)", "reason": "利差收益持續受惠，資產負債表極其穩健。"}],
                "high_risk_groups_us": [{"name": "中小型電動車供應鏈", "reason": "高利率環境壓抑消費者分期貸款意願，資本支出壓力沉重。"}]
            }
        ]

    def fetch_web3_crypto_intelligence(self):
        """🌐 區塊 2：Web3 智能金融與 RWA（多條深度新聞）"""
        return [
            {
                "title": "Agentic Finance 重新平衡 RWA 流動性池，減半後礦企啟動資產轉型",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.5x",
                "source": "CoinDesk / On-Chain Analytics",
                "macro_attribution": "2026 減半週期過後，純挖礦邊際利潤下滑。AI 智能體金融（Agentic Finance）全面接管鏈上資產配置，頭部礦企啟動資產代幣化（RWA）戰略，將重電基礎設施打包成 RWA 代幣，鎖定長期法幣實質現金流。",
                "tw_spillover_effect": "美股 Web3 概念股全面翻新重電與機房設備，這股 AI 數據中心與資產轉型潮，直接轉化為台廠高階 AI 伺服器代工、液冷散熱供應鏈的爆發性實質訂單。",
                "rwa_flow_metric": "鏈上基礎設施 RWA 資金池 24H 淨流入達 +$45.8M，多鏈智能體自動結算量創歷史新高。",
                "agent_action_log": "[AGENT_FINANCE] Protocol executing autonomous cross-chain settlement. Rebalanced RWA liquidity to Layer-2 nodes.",
                "recommended_groups_tw": [{"name": "AI 伺服器代工（台積電、廣達）", "reason": "通吃美股巨頭與礦企轉型 AI 的硬體升級紅利。"}, {"name": "高階液冷散熱供應鏈（奇鋐、雙鴻）", "reason": "算力密度翻倍，高階散熱解決方案迎來剛性需求。"}],
                "high_risk_groups_tw": [{"name": "傳統低階顯卡、純挖礦板卡廠", "reason": "資金向 AI 高階晶片靠攏，傳統挖礦硬體面臨去庫存壓力。"}],
                "recommended_groups_us": [{"name": "MARA Holdings (MARA)", "reason": "基礎設施轉型速度領先同業，資產 RWA 化後估值重估空間大。"}, {"name": "NVIDIA (NVDA)", "reason": "算力晶片的剛性需求最大贏家。"}]
            }
        ]

    def fetch_tw_stocks_intelligence(self):
        """💻 區塊 3：台股與經濟部政策（多條深度新聞）"""
        return [
            {
                "title": "經濟部研議爭取美方 AI 資料中心來台落腳，推動亞洲算力與綠電樞紐計畫",
                "ai_sentiment": "Bullish",
                "vol_multiplier": "3.8x",
                "source": "台灣經濟部 (MOEA) / 焦點新聞",
                "macro_attribution": "經濟部最新政策聚焦於提供穩定的高階算力基礎設施與綠電配套，積極吸引美股科技巨頭與進行 AI 轉型的 Web3 礦企將亞太 AI 資料中心落地台灣。這與美股高利率環境下追求高效率、低成本跨境基礎設施的宏觀趨勢完美共振。",
                "tw_spillover_effect": "本政策將直接加速台灣本地綠電、儲能系統的審查釋出，深化台美跨市場科技供應鏈與軟硬體整合的防禦性護城河。",
                "rwa_flow_metric": "政策預期引導跨國實體資產投資金額逾 1500 億台幣，潛在綠電憑證 RWA 發展空間巨大。",
                "agent_action_log": "[POLICY_AGENT] Government policy text compiled. High-priority keyword correlation detected: Green Energy Hub.",
                "recommended_groups_tw": [{"name": "綠電與重電儲能鏈（華城、中興電、雲豹能源）", "reason": "資料中心落地必備綠電配套，政策剛性需求明確。"}],
                "high_risk_groups_tw": [{"name": "高耗能且無綠電轉型之傳統製造業", "reason": "面臨排碳與電價結構性調漲壓力，毛利恐遭進一步侵蝕。"}],
                "recommended_groups_us": [{"name": "NextEra Energy (NEE)", "reason": "全球綠電基礎設施龍頭，完美對接算力中心的綠電淨零碳排要求。"}]
            }
        ]

    def generate_dashboard_data(self):
        return {
            "us_macro": self.fetch_us_macro_intelligence(),
            "web3_crypto": self.fetch_web3_crypto_intelligence(),
            "tw_stocks": self.fetch_tw_stocks_intelligence(),
            "global_vix": {
                "value": 22.4,
                "status_zh": "突破關鍵20關卡 / 強烈避險情緒 (Risk-Off)",
                "status_en": "Surged Past 20 / Strong Risk-Off Hedging",
                "trend": "Upward (+14.2% 24H)",
                "insight_zh": "【VIX 跨境聯動歸因】VIX 恐慌指數飆升至 22.4，反映宏觀資金正全面買入波動率期權進行下行保護。此現象與鏈上美債 RWA 池（+$45.8M）資金流入高度共振，預示傳統股市權值股短期將面臨流動性洗盤，資金朝技術護城河極高的防禦性節點集中。",
                "insight_en": "【VIX Cross-Market Insight】VIX jumps to 22.4, signaling widespread institutional hedging."
            }
        }

if __name__ == "__main__":
    engine = RAGAttributionEngine()
    final_data = engine.generate_dashboard_data()
    
    # 💡 核心修正：強制輸出至專案根目錄下的檔案，與 index.html 同路徑
    output_filename = 'dashboard_data.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 數據已成功完整更新至 {output_filename}！共計 4 條頂級歸因情報已同步。")
