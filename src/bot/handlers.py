from pyexpat.errors import messages

from .client import TelegramClient
from .bot_type import Message, Update
from .schemas import MessageIn

async def update_handler(update: Update, client: TelegramClient):
    if update.message and update.message.text:
        message: Message = update.message
        chat_id = message.chat.chat_id
        message_response = MessageIn(chat_id=chat_id, text=message.text)
        await client.send_message(message_response)