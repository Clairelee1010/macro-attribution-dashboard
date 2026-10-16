> 歷史修正說明：GTA-002 保留原城市為主首頁，新版移至 `play.html`。以 `GTA-002-START-HERE.md` 為準。

# RESTORE-001 · 404 修正與原研究介面恢復

## 原因與這份修正的範圍

使用者截圖顯示首頁可載入，但新功能進入 GitHub Pages「File not found」。這證明目的頁面沒有成功提供，還不能單憑截圖判斷是新增資料夾未上傳、發佈來源設定、漏包或部署尚未完成。交付環境無法讀取線上網站，因此不宣稱已確認線上根因或修復部署。

本次把主要新功能改為首頁內 hash 路由，減少新增資料夾頁面依賴。完整新功能由 `index.html` + `assets/` 載入。仍附原本子目錄頁面作為相容入口。

| 功能 | 新主要入口 |
| --- | --- |
| 任務大廳 | `./` |
| 原研究首頁（城市介面） | `research-dashboard.html` |
| 原宏觀研究 | `p01/` |
| 原預測市場 | `p02/` |
| 原整合研究 | `intelligence/` |
| 原代理情報 | `p03/` |
| 原每日研究／Robi 頁 | `daily/` |
| 原總覽 | `overview/` |
| 證據任務 | `./#/workbench` |
| 代理支出沙盒 | `./#/agent` |
| 筆記 | `./#/journal` |
| Product Lab | `./#/product-lab` |
| Trade Clarity | `./#/trade-clarity` |
| 學習世界 | `learn/` |
| 發布檔案檢查 | `site-check.html` |

## 原研究介面恢復方式

從使用者 `(45)(1).zip` 還原 P01、P02、P02-web、整合情報、P03、daily、overview 的 HTML，移除上一版整頁轉址。原首頁保存在根目錄的 `research-dashboard.html`，因此原有相對路徑仍成立。

每個原研究頁新增獨立的導覽列，可返回任務大廳或 Product Lab。導覽使用 Shadow DOM，減少干擾原 CSS。研究原型的限制會清楚顯示：規則分數和關聯摘要不是已驗證因果或套利。原研究引擎、JSON 和 AI Worker 未被改寫；恢復介面不代表舊 AI 問答已上線驗收。

## 安裝：不要把檔案平鋪到同一個資料夾

1. 解壓本 ZIP。
2. 開啟裡面的 `repository-files/`。
3. 將**裡面的內容**放到 GitHub repository 根目錄，保留資料夾結構。`index.html` 要在最外層；JS、CSS 要在 `assets/`。既有檔案覆蓋，缺少的新增。
4. 不要刪除其他檔案。不要把外層 `repository-files/` 也當成網站根目錄上傳。
5. 提交並等待 Pages 部署成功。
6. 重新整理首頁（Windows: Ctrl+F5），再操作入口。新首頁的主要 JS/CSS 已加版號以避開舊快取。
7. 打開 `https://clairelee1010.github.io/macro-attribution-dashboard/site-check.html`，按「檢查發布檔案」。出現 404 的路徑必須依同一路徑補上。
8. 執行 **Web3 Fieldwork acceptance**；此環境未代替你執行 GitHub Actions。

### GitHub 上傳結構核對

- 根目錄：`index.html`、`research-dashboard.html`、`site-check.html`
- `assets/`：`fieldwork-core.js`、`fieldwork.js`、`fieldwork.css`、`product-lab.js`、`product-lab.css`、`trade-engine.js`、`research-bridge.js`
- 舊頁面：`p01/index.html` 等放在各自原本資料夾
- `learn/`：保留學習世界完整檔案

本 ZIP 已包含原先新增功能所需檔案，可補齊可能漏傳的檔案。沒有行情或新聞 JSON，沒有 Worker 機密，無須刪檔。若線上有比 `(45)` 更新的研究介面變更，這些還原頁面會以 `(45)` 為準，請先備份 repository。

## 驗證結果與限制

52 / 52 項 Node / jsdom 測試通過。其中 5 項新增路由回歸測試檢查：首頁直接打開所有新功能、hash 切換、上一頁返回、Product Lab 區段連結、原研究頁不再轉址及 P02 來源同步。原研究頁的本地 script/style 路徑也已核對存在。

另保留既有 47 項學習、研究、政策、交易測試。結果在 `docs/RESTORE-001-TEST-RESULTS.txt`。

未執行真實瀏覽器或手機視覺驗收，未發布至你的帳戶，也未確認線上 HTTP 狀態。已更新 CI 瀏覽器腳本使用 hash 路由，供上傳後執行。所有先前版本的說明檔屬歷史紀錄；部署與網址以本文件為準。
