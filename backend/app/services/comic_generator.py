"""AI 漫畫生成服務。

負責把使用者的文字日記轉換成漫畫：
1. 總結當天事件
2. 分鏡成多個漫畫分格
3. 為每個分格生成圖片
4. 產生無障礙口述影像文字

目前為骨架 / stub 實作，實際串接 AI 模型時再補上。
"""

from app.core.config import Settings
from app.models.comic import ComicPanel, ComicResult, DiaryEntry


class ComicGenerator:
    """將日記文字轉為漫畫的服務。"""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def summarize(self, text: str) -> str:
        """把當天描述總結成適合做漫畫的簡短敘事。

        TODO: 串接 LLM（OpenAI / Gemini 等）。
        """
        # 佔位實作
        return text.strip()[:200]

    async def generate_panels(self, summary: str) -> list[ComicPanel]:
        """依總結內容生成漫畫分格與圖片。

        TODO: 呼叫文字轉圖片模型，並填入每格的 alt_text。
        """
        # 佔位實作
        return [
            ComicPanel(
                order=1,
                image_url="",
                caption=summary,
                alt_text=f"畫面描述：{summary}",
            )
        ]

    async def build_narration(self, panels: list[ComicPanel]) -> str:
        """把各分格的 alt_text 串成整篇無障礙口述影像。"""
        return " ".join(p.alt_text for p in panels if p.alt_text)

    async def create_comic(self, entry: DiaryEntry) -> ComicResult:
        """完整流程：日記 -> 漫畫。"""
        summary = await self.summarize(entry.text)
        panels = await self.generate_panels(summary)
        narration = await self.build_narration(panels)
        return ComicResult(
            user_id=entry.user_id,
            summary=summary,
            panels=panels,
            narration=narration,
        )
