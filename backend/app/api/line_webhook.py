"""LINE Bot webhook 路由。

接收 LINE 平台的訊息事件，將使用者的日記文字轉成漫畫，
並回傳結果給使用者。
"""

import logging

from fastapi import APIRouter, Header, HTTPException, Request
from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.core.config import get_settings
from app.models.comic import DiaryEntry
from app.services.comic_generator import ComicGenerator

logger = logging.getLogger(__name__)
router = APIRouter(tags=["line"])


@router.post("/webhook")
async def line_webhook(
    request: Request,
    x_line_signature: str = Header(default=""),
) -> dict:
    """LINE Messaging API 的 webhook 進入點。"""
    settings = get_settings()
    if not settings.line_channel_secret or not settings.line_channel_access_token:
        raise HTTPException(status_code=503, detail="LINE 憑證尚未設定")

    body = (await request.body()).decode("utf-8")
    parser = WebhookParser(settings.line_channel_secret)

    try:
        events = parser.parse(body, x_line_signature)
    except InvalidSignatureError as exc:
        raise HTTPException(status_code=400, detail="簽章驗證失敗") from exc

    configuration = Configuration(access_token=settings.line_channel_access_token)
    generator = ComicGenerator(settings)

    async with AsyncApiClient(configuration) as api_client:
        line_api = AsyncMessagingApi(api_client)
        for event in events:
            if isinstance(event, MessageEvent) and isinstance(
                event.message, TextMessageContent
            ):
                await _handle_text_message(event, line_api, generator)

    return {"status": "ok"}


async def _handle_text_message(
    event: MessageEvent,
    line_api: AsyncMessagingApi,
    generator: ComicGenerator,
) -> None:
    """處理使用者傳來的文字日記。"""
    entry = DiaryEntry(user_id=event.source.user_id, text=event.message.text)
    result = await generator.create_comic(entry)

    # TODO: 之後改為回傳含圖片的漫畫訊息（ImageMessage / Flex Message）
    reply_text = f"今天的漫畫總結：\n{result.summary}"
    await line_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=reply_text)],
        )
    )
