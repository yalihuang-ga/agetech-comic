# 開發指南

## 待辦與擴充方向

### AI 漫畫生成（backend/app/services/comic_generator.py）
目前為 stub，需串接實際模型：
- `summarize()`：用 LLM 把長輩的口語日記整理成適合漫畫的敘事。
- `generate_panels()`：呼叫文字轉圖片模型（例如 DALL·E、Imagen、SD），
  並為每格填入 `caption` 與無障礙 `alt_text`。
- `build_narration()`：組合各分格描述成整篇口述影像。

### LINE Bot（backend/app/api/line_webhook.py）
- 目前只回傳文字總結，之後改為回傳含圖片的訊息
  （`ImageMessage` 或 Flex Message 呈現多格漫畫）。
- 可加入語音輸入（LINE 的 audio message + STT）讓長輩用說的。

### 無障礙
- 漫畫每格都要有 `alt_text`。
- 前端呈現時，圖片需帶 `alt`，並提供「播放口述」按鈕（可接 TTS）。
- 遵循 WCAG：足夠對比、大字體、鍵盤可操作。

## 前後端協作

- 後端提供 `POST /comics/generate`，前端（PM）用 `frontend/src/lib/api.ts` 呼叫。
- 資料模型定義在 `backend/app/models/comic.py`，前端型別對應在 `frontend/src/lib/api.ts`，
  兩邊修改時請保持一致。

## 環境變數

- 後端：`backend/.env`（參考 `.env.example`）— LINE 與 AI 憑證。
- 前端：`frontend/.env.local`（參考 `.env.example`）— 後端 API 位址。
- **切勿**把含真實金鑰的 `.env` 提交到 git。
