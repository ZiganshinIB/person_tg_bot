from typing import Optional, Union, List

from pydantic import BaseModel, Field

from .bot_type import MessageEntity, ReplyParameters, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    ForceReply


class MessageIn(BaseModel):
    business_connection_id: Optional[str] = Field(
        None,
        description="Уникальный идентификатор бизнес -соединения от имени которого будет отправлено сообщение",
    )
    chat_id: Union[int, str] = Field(
        description="Уникальный идентификатор чата или имя пользователя",
    )
    message_thread_id: Optional[int] = Field(
        None,
        description="Уникальный идентификатор потока сообщений."
                    "Только для форума супергруппы",
    )
    text: str = Field(
        description="Текст сообщения, который будет отправлен, 1-4096 символов после разбора сущностей",
    )
    parse_mode: Optional[str] = Field(
        None,
        description="Режим разбора сущностей",
    )
    entities: Optional[List[MessageEntity]] = Field(
        None,
        description="Сущности в сообщении",
    )
    disable_web_page_preview: Optional[bool] = Field(
        None,
        description="Отключить предварительное просмотр URL-адреса",
    )
    disable_notification: Optional[bool] = Field(
        None,
        description="Отключить уведомление",
    )
    protect_content: Optional[bool] = Field(
        None,
        description="Защитить содержимое сообщения от спама",
    )
    allow_paid_broadcast: Optional[bool] = Field(
        None,
        description="Разрешить отправку сообщения в бесплатном режиме",
    )
    message_effect_id: Optional[str] = Field(
        None,
        description="Уникальный идентификатор эффекта",
    )
    reply_parameters: Optional[ReplyParameters] = Field(
        None,
        description="Параметры ответа",
    )
    reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]] = Field(
        None,
        description="Клавиатура",
    )


