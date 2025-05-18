from contextlib import suppress

from tg_api import (
    SyncTgClient,
    SendMessageRequest,
    GetUpdatesRequest,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from config import settings

token = settings.BOT_TOKEN.get_secret_value()


def handle_update(update: Update) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='button_1', callback_data='test'),
                InlineKeyboardButton(text='button_2', callback_data='test'),
            ],
        ],
    )
    if update.message and update.message.text:
        message: SendMessageRequest = SendMessageRequest(
            chat_id=update.message.chat.id,
            text=update.message.text,
            reply_markup=keyboard,
        )
        message.send()


def main() -> None:
    with SyncTgClient.setup(token):
        tg_request = GetUpdatesRequest(timeout=30)
        for update in tg_request.listen_to_updates():
            handle_update(update)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        main()
