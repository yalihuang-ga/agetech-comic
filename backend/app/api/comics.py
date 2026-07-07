"""供前端（Next.js）使用的漫畫 API 路由。

PM 開發的前端介面可呼叫這些端點來測試 / 展示漫畫生成，
不必透過 LINE 平台。
"""

from fastapi import APIRouter

from app.core.config import get_settings
from app.models.comic import ComicResult, DiaryEntry
from app.services.comic_generator import ComicGenerator

router = APIRouter(prefix="/comics", tags=["comics"])


@router.post("/generate", response_model=ComicResult)
async def generate_comic(entry: DiaryEntry) -> ComicResult:
    """從日記文字生成漫畫（供前端直接呼叫）。"""
    generator = ComicGenerator(get_settings())
    return await generator.create_comic(entry)
