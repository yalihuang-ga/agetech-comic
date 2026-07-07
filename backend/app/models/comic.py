"""漫畫生成相關的資料模型。"""

from pydantic import BaseModel, Field


class DiaryEntry(BaseModel):
    """使用者描述當天做了什麼事情的一則日記。"""

    user_id: str = Field(..., description="LINE 使用者 ID")
    text: str = Field(..., description="使用者描述當天發生的事情（文字）")


class ComicPanel(BaseModel):
    """漫畫的單一分格。"""

    order: int = Field(..., description="分格順序")
    image_url: str = Field(..., description="生成圖片的網址")
    caption: str = Field("", description="分格說明文字")
    # 無障礙：供螢幕報讀器或口述影像使用的替代文字
    alt_text: str = Field("", description="供無障礙口述使用的畫面描述")


class ComicResult(BaseModel):
    """一天的完整漫畫總結結果。"""

    user_id: str
    summary: str = Field(..., description="當天事件的文字總結")
    panels: list[ComicPanel] = Field(default_factory=list)
    # 整篇漫畫的口述影像（無障礙）
    narration: str = Field("", description="整篇漫畫的無障礙口述內容")
