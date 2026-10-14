# AI-006：Gemini Robi 市場問答

## 實際狀態
程式可部署；尚未取得金鑰、部署後端或做真實 Gemini 呼叫。只上傳 GitHub 不會啟用 AI。原有摘要仍可用。

## 1. 免費 Gemini 金鑰
在 https://aistudio.google.com/apikey 建立或選擇 Free tier 專案金鑰，不啟用 Cloud Billing。不要貼到對話、GitHub、ai-config.js。固定模型 gemini-2.5-flash-lite，官方目前列有 Free Tier，但帳戶配額／模型可用性仍以 AI Studio 為準；模型相同不代表付費專案也免費。

## 2. 部署 Worker
需要 Cloudflare 帳號及 Node.js。ai-worker 目錄中執行：

```
npx wrangler login
npx wrangler secret put GEMINI_API_KEY
npx wrangler deploy
```
secret 指令會在本機安全提示輸入金鑰。若首次尚未建立 Worker 而 secret 指令詢問建立服務，依提示建立；也可先 deploy 再 secret put。這些動作由你在本機執行，未在本次執行。
使用 Cloudflare Workers Free 方案；Durable Object 採 SQLite binding。啟用前檢查 Cloudflare 當前免費限制，勿升級付費方案。後端是独立服務，不是 GitHub Pages 功能。

## 3. 前端網址
部署成功後取得 https://claire-market-robi.<你的子網域>.workers.dev 。在 daily/ai-config.js 將 ROBI_API_URL 空字串換成該 HTTPS 網址，不包含 /ask。只填公開網址。

## 4. 上傳 GitHub
覆蓋 daily/index.html、README.md；新增 daily/ai-config.js、daily/ai-chat.js、ai-worker/、AI-006-README.md。保留之前 SITE-005 字體與 daily/app.js 更新。不要上傳 .dev.vars 或任何金鑰檔。ai-worker/.gitignore 僅保護 git，GitHub 網頁拖曳上傳仍須人工避免秘密檔案。

## 5. 驗收
開 daily，展開 Robi；詢問 BTC 最新資料，確認回答引用 ID 與來源連結。再測沒資料、過期、取消及服務不可用的情境。Gemini 429 或應用上限顯示額度提示；改用快速摘要。

## 實作範圍
- 後端只讀取固定 GitHub Pages 的公開行情與新聞 JSON，最多五則新聞、問題 500 字，最多四個自選代碼。
- 模型輸出分類事實／推論／不足證據；要求附 [ID]。程式驗證引用存在，不驗證每個句子必然被來源支持。
- 可用的研究語料仍限 P01 行情／新聞；P02/P03 全量資料尚未加入。
- 應用上限由 Durable Object 保存：全站每日 50 次，每個 IP 每日 5 次（UTC 日期），失敗請求也計次；不等同 Google 官方配額。
- Origin 白名單不是使用者認證，仍可能被偽造；全站上限用於控制耗用。
- 限短回答、無搜尋工具、無模型自動備援、無交易執行。未加入共享回答快取。
- 免費 Gemini 可能使用提交內容改善產品，請只問公開市場資訊，不輸入私人資料。自選代碼會傳後端與模型。
- 沒有任何程式能保證已啟用付費 Billing 的 Google 專案零費用，請確認 Free tier。

## 已完成測試
JS 語法、來源整理、Origin 拒絕、未設定、長度限制、持久用量限制、模擬 Gemini 引用回答；未完成正式後端部署、真實模型回覆與瀏覽器視覺驗證。
