import pytest
from bot.client import TelegramClient
from bot.schemas import MessageIn

@pytest.mark.asyncio
async def test_send_message(httpx_mock):
    httpx_mock.add_response(json={"ok": True, "result": {"message_id": 1}})
    client = TelegramClient("fake-token")
    msg = MessageIn(chat_id=123456, text="Привет!")
    response =  await client.send_message(msg)
    assert response["ok"] is True

