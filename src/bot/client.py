from urllib.parse import urljoin
from .schemas import MessageIn

import httpx


class TelegramClient:
    def __init__(self, token: str):
        self.base_url = f"https://api.telegram.org/bot{token}"

    async def send_message(self, message: MessageIn):
        """Отправка сообщения через Telegram API."""
        url = urljoin(self.base_url, "sendMessage")
        payload = {"chat_id": chat_id, "text": text}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.raise_for_status()