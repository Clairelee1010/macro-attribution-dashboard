# DAILY-001：今日情報與瀏覽器追蹤

## 更新
- 新增 `/daily/`：近期重點、歷史資訊、證據詳情、自選資產、追蹤紀錄與 JSON 匯出。
- 城市首頁加入今日情報入口，保留既有模組。
- 使用既有五份 JSON；不新增 API、AI 呼叫、會員系統或交易功能。
- 近期條件為觀測／事件時間距現在 36 小時內，未來時間容差 5 分鐘。新聞另排除來源標示 STALE；超時顯示於歷史區。
- 新聞採原有 relevance_score 排序，其後依資料時間排列。不同類型分數不混合；熱度不視為勝率。
- 自選與追蹤保存在 localStorage，限同瀏覽器，清除瀏覽器資料會移除。可匯出 JSON；目前沒有匯入功能。
- 價格追蹤採觀察清單最新歷史點日期，而非檔案產生時間；僅同資產、較新時間且有效非零基準才計算變化。

## 上傳 GitHub
1. 將更新 ZIP 解壓縮。
2. 在原 repository 上傳 `daily/`、根目錄 `index.html`、本說明檔及 README.md，保持目錄結構。GitHub 網頁 Upload files 可拖入 daily 資料夾。
3. Commit 後等待既有 GitHub Pages 部署完成。
4. 開啟 https://clairelee1010.github.io/macro-attribution-dashboard/daily/ 。此網址須上傳及部署後才會提供新頁。
5. 資料仍由原 GitHub Actions 更新。頁面重新讀取只讀取已產生 JSON，不觸發外部行情抓取。

## 本機
在 repository 根目錄執行 `python -m http.server 8000`，開啟 http://localhost:8000/daily/ 。不可直接以 file:// 開啟，因 fetch 需要 HTTP。

## 驗證與限制
已檢查 JavaScript 語法、五個輸入 JSON 的相容欄位及相對路徑。未執行瀏覽器視覺驗證或外部 API 正確性驗證。日期與數據沿用來源檔案，沒有修改原始行情；此更新不代表來源數據已獲獨立驗證。
