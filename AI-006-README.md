# Robi Gemini 問答 — 2026-10-16 更新

最新狀態、來源範圍與限制以 [README](README.md) 與 [發布／驗收說明](RELEASE-2026-10-16.md) 為準。

- 前端：`daily/ai-config.js`、`daily/ai-chat.js`。
- 後端：`ai-worker/worker.mjs`、`ai-worker/wrangler.toml`。
- 只有自由問答會呼叫 Gemini；快速摘要、P03 關鍵字回應仍是規則。
- `/health` 只驗證設定是否存在，不證明金鑰有效或模型能回答。
- 本次測試連線的正式服務回傳 Cloudflare `403 / 1010`。尚未完成新版後端部署及真實 Gemini 回覆驗收。
- 前端和 Worker 要一起更新；只覆蓋 GitHub 檔案不會更新 Cloudflare Worker。
- 保留原有 secret，不把金鑰放進 GitHub、設定 JS、診斷資訊或對話。
- 部署前確認使用正確 Cloudflare 帳號。若原本 secret 不存在，在本機使用 `npx wrangler secret put GEMINI_API_KEY` 的安全輸入提示設定。
- 問題及部分自選代碼會送往後端與 Gemini，僅使用公開資料。不承諾免費專案永久免費或已開啟帳單的專案零費用。
