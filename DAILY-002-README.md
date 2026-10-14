# DAILY-002：統一行情與自選情報

## 上傳
將更新包內 index.html、assets/market-snapshot.js、assets/home007-neon-city.js、daily/ 的四個檔案及 README／本說明上傳至原專案相同路徑。不要刪除其他 assets 或 daily 資料。重新載入兩個頁面（Ctrl+F5）。

## 行情規則
BTC/ETH 兩頁及自選清單統一讀 live_market_data.json，同一筆價格、漲跌幅及 observed_at。資料缺失顯示 N/A，不退回另一來源。其他資產使用 multi_asset_watchlist.json 同一筆資料，不使用多來源中位數。首頁滑鼠停在價格可查看來源與時間，頁尾亦列觀測時間。頁面載入若跨越一次資料更新，仍可能讀到不同快照；比較前請重新讀取兩頁並核對時間。本修正不改行情 API、原始 JSON 或 GitHub Actions。

## 與我相關
先到自選資產點星號，再於今日情報選「與我相關」。以標題中的獨立代碼、名稱別名或來源明確資產欄位配對；顯示配對原因。一般宏觀新聞不自動配對到所有股票／加密貨幣。沒有配對時顯示空狀態，不補造內容。歷史區也套用相同篩選，原追蹤紀錄不刪除。

## 驗收
檢查兩頁 BTC/ETH 同時間數值一致；BTC 星號應配對 Bitcoin/BTC／BTC 熱區，取消後立即重新篩選；ETH 不應匹配文字中的 tether，SOL 不應匹配 solution；過期資料僅出現在歷史區。追蹤價格只比較同資產較新快照，不代表投資績效。

未執行瀏覽器視覺測試。已有 JavaScript 語法及資料規則測試；無交易或新 AI API 呼叫。
