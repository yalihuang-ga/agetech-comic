/**
 * 後端 API 串接工具。
 *
 * 後端預設跑在 http://localhost:8000（見 backend/ 說明）。
 * 可透過環境變數 NEXT_PUBLIC_API_BASE_URL 覆寫。
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export interface DiaryEntry {
  user_id: string;
  text: string;
}

export interface ComicPanel {
  order: number;
  image_url: string;
  caption: string;
  /** 供無障礙口述影像使用的畫面描述 */
  alt_text: string;
}

export interface ComicResult {
  user_id: string;
  summary: string;
  panels: ComicPanel[];
  /** 整篇漫畫的無障礙口述內容 */
  narration: string;
}

/** 呼叫後端，把一天的日記文字轉成漫畫。 */
export async function generateComic(entry: DiaryEntry): Promise<ComicResult> {
  const res = await fetch(`${API_BASE_URL}/comics/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(entry),
  });

  if (!res.ok) {
    throw new Error(`漫畫生成失敗：${res.status}`);
  }

  return res.json();
}
