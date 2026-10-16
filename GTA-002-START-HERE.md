# GTA-002 · 原 GTA 首頁＋新版互動功能

保留原 GTA 城市首頁作為主入口，另串回新版互動功能。

| 功能 | 上傳後的網址路徑 |
| --- | --- |
| 原 GTA 城市首頁 | `/macro-attribution-dashboard/` |
| 新版任務大廳 | `/macro-attribution-dashboard/play.html` |
| 學習世界 | `/macro-attribution-dashboard/learn/` |
| 證據偵探 | `/macro-attribution-dashboard/play.html#/workbench` |
| 代理守門員 | `/macro-attribution-dashboard/play.html#/agent` |
| 筆記 | `/macro-attribution-dashboard/play.html#/journal` |
| Product Lab | `/macro-attribution-dashboard/play.html#/product-lab` |
| Trade Clarity | `/macro-attribution-dashboard/play.html#/trade-clarity` |

## 使用方式

原首頁保留城市畫面、研究導覽與熱區。右下角新增「探索新版功能」可展開選單。新版放在 `play.html`，不取代 GTA 首頁；新功能使用 `play.html#/…`，避免依賴新增子目錄頁面。新版與學習頁提供返回 GTA 首頁和任務大廳的入口。舊根目錄 `#/workbench` 等書籤會轉到新的 `play.html#/workbench`。

研究頁依使用者提供 `(45)` 版本恢復；不代表舊 AI 問答或所有研究結論已驗證。

## 安裝

1. 先備份 GitHub 專案。
2. 解壓，把 `repository-files/` **裡面的內容**按原路徑上傳至專案根目錄。
3. 既有檔案覆蓋，沒有的新增；不要刪除其他資料，不要把 JS/CSS 平鋪到根目錄。
4. 根目錄必須有 `index.html`（GTA）及 `play.html`（新版大廳）。`assets/research-bridge.js` 為 GTA 選單及跨頁導覽。
5. 等待 Pages 部署成功，Ctrl+F5 後展開右下角「探索新版功能」。
6. 若仍有 404，開 `site-check.html` 檢查必要檔案發布狀態。

這是累積整合補丁，已包含先前新功能與研究介面恢復所需檔案，不用再套前幾份。補丁不含行情／新聞 JSON、不修改 Python 管線或 Worker。若線上研究 HTML 有比 `(45)` 更新的變更，請先比較再覆蓋。

## 驗證與限制

54 / 54 項 Node/jsdom 測試通過，包含原 GTA 主頁保留、雙語選單、新功能入口、路由返回、學習與交易／政策規則。結果在 `docs/GTA-002-TEST-RESULTS.txt`。

尚未代替你部署，未執行真實瀏覽器／手機視覺驗收。CI 腳本已更新 `play.html` 路徑，仍需上傳後執行。原 GTA 城市的既有手機橫向呈現方式保留，本次未重新設計城市素材或宣稱完成手機視覺改善。

交易、政策、區塊練習是教學模擬；Robi 導覽與風險解釋為預寫／規則文案，沒有新增生成式 AI 串接。
