# 這是您目前應該要有的「動態數據源」結構 (請檢查是否為此形式)
def fetch_us_macro_intelligence(self):
    # 這裡請確保它是連接到真實 API 或自動抓取程序的，而不是寫死的字串！
    # 範例：如果新聞是舊的，請把這裡改成 API 請求 (如 requests.get...)
    return [
        {
            "title_zh": "從 API 獲取的新聞標題",
            "macro_attribution_zh": "從 API 獲取的最即時分析...",
            "rec_title_us": "...",
            "risk_title_tw": "..."
        }
    ]
