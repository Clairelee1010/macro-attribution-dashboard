# LEARN-003 · Web3 Learning Playground

以 `macro-attribution-dashboard-main (43).zip` 為基礎，將現有官方資源導覽補上本機互動練習。此增修只更新學習頁，不覆蓋行情、Robi Worker、來源品質或其他頁面。

## 新增體驗

- 動態區塊插畫：CSS 製作，支援暫停及 prefers-reduced-motion；沒有外部動畫套件。
- 區塊鏈實驗室：加入教學交易、打包最多 3 筆交易／區塊、SHA-256 指紋、前區塊連結、竄改與鏈驗證。重設會中止進行中的打包。
- 錢包安全任務：四個情境，選擇後提供原因。全部正確完成才取得該任務徽章。
- AI 學習提問卡：選主題、程度與說明方式，組合中英文提問稿。支援複製及無剪貼簿權限時的手動選取。
- 四項學習徽章與本機進度；交易明細不寫入儲存。中英文切換保留實驗及測驗進度。
- 原有八個官方資源、三條路徑及獨立 Blockchain Learning Explorer 連結保留。

## 界線

本機交易是教學模擬，不連接錢包、不轉移資產，也不模擬完整共識。SHA-256 只示範資料指紋，不能當成 Ethereum 區塊編碼或整條鏈安全性的實作。真實系統依賴簽名、共識、節點驗證與其他規則。

AI 提問卡是**本機字串組合工具**，不是模型回答。沒有任何 AI API 呼叫，不需要金鑰。使用者自行複製後才會提交到自己選用的 AI 工具。模型後續回答仍需核對官方來源。

教材摘要與建議不等於官方認證。安全測驗的徽章是本機練習記錄，不是安全資格。

## 更新哪幾個檔案？

| 路徑 | 操作 |
|---|---|
| `learn/index.html` | 覆蓋原檔 |
| `learn/lab.css` | 新增 |
| `learn/lab.js` | 新增 |
| `learn/UPDATE-LEARN-003.md` | 新增說明 |
| `tests/learn/lab.test.cjs` | 新增行為測試 |
| `tests/learn/browser-acceptance.mjs` | 新增瀏覽器測試 |
| `.github/workflows/learn_acceptance.yml` | 新增 GitHub 自動驗收 |

先前 (43) 版本的 package.json / package-lock.json 已含 jsdom、playwright；本次不更動這兩份檔案。不能把本更新包當成完整程式庫使用。

將壓縮包內 `macro-attribution-dashboard/` 裡的內容合併到原 repo 根目錄，同名覆蓋、保留目錄結構。不要把外層資料夾上傳成網站子目錄。保留原本 `.github` 的其他 workflow。

GitHub Pages 成功發布後，開啟 `/learn/` 並重新整理快取。無需更新 Worker 或 API 金鑰。

## 實際驗證

本次 9 項 Node / jsdom 行為測試全部通過：

1. SHA-256 固定向量與創世區塊。
2. 交易整數上下限、池容量及前區塊雜湊連結。
3. 竄改後目前與後續鏈失效，重設保留徽章。
4. 重設阻止正在執行的打包附加舊區塊。
5. 中英文切換不清空交易。
6. 安全任務需四題正確完成。
7. 提問稿產生、雙語與剪貼簿失敗處理。
8. 鍵盤分頁與動畫開關的可及狀態。
9. 無儲存權限／無 Web Crypto 時的降級。

新增 JS / 瀏覽器測試語法及 HTML 唯一 ID 已檢查。**本次未做真實瀏覽器視覺驗收。**依 Sites 技能要求「If $control-browser is unavailable, skip browser QA」，本環境沒有該能力，因此未改用其他瀏覽器路徑宣稱通過。

GitHub Actions 的 `Web3 Learning Lab acceptance` 會執行 DOM 測試，以及 Chromium 320 / 375 / 768 / 1280px 的版面與互動驗收；這份流程尚待上傳後執行。

本機檢查：

```bash
npm ci
node --test tests/learn/lab.test.cjs
npx playwright install --with-deps chromium
node tests/learn/browser-acceptance.mjs
```

## 教學來源

- https://ethereum.org/en/developers/docs/blocks/
- https://ethereum.org/en/developers/docs/transactions/
- https://ethereum.org/en/security/

以上來源於 2026-10-16 查閱，用於概念核對；頁面為原創教學模擬與摘要，不重製完整官方教材。
