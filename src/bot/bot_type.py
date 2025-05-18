from enum import Enum
from typing import Optional, Literal, List

from pydantic import BaseModel, Field, AnyUrl, root_validator, AnyHttpUrl


class EntityType(Enum):
    MENTION = "mention"
    HASHTAG = "hashtag"
    CASHTAG = "cashtag"
    BOT_COMMAND = "bot_command"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    TEXT_MENTION = "text_mention"
    CUSTOM_EMOJI = "custom_emoji"

class ChatType(Enum):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


LanguageCode = Literal[
    "af", "ak", "am", "ar", "arn", "as", "az",
    "ba", "be", "bg", "bh", "bo", "br", "bs",
    "ca", "ckb", "co", "cs", "cy",
    "da", "de","dsb", "dv",
    "el", "en", "es", "et", "eu",
    "fa", "fi", "fil", "fo", "fr", "fy",
    "ga", "gd", "gil", "gl", "gsw", "gu",
    "ha", "he", "hi", "hr", "ht", "hu", "hy",
    "ig", "ii", "is", "it", "ja",
    "ka", "kk", "kl", "km", "kn", "ko", "kok", "ku", "ky",
    "lb", "lo", "lt", "lv",
    "mi", "mk", "ml", "mn", "moh", "mr", "ms", "mt", "my",
    "nb", "ne", "nl", "nn", "no",
    "oc", "or", "pap", "pa", "pl", "prs", "ps", "pt", "quc", "qu",
    "rm", "ro", "ru", "rw",
    "sa", "sah", "se", "si", "sk", "sl", "sma", "smj", "smn", "sms", "sq", "sr", "st", "sv", "sw",
    "ta", "te", "tg", "th", "tk", "tn", "tr", "tt", "tzm",
    "ug", "uk", "ur", "uz", "vi", "wo", "xh", "yo", "zh", "zu"
]


class User(BaseModel):
    user_id: int = Field(
        alias="id",
        description="Уникальный идентификатор пользователя",
    )
    is_bot: bool = Field(
        True,
        description="Является ли пользователь ботом",
    )
    first_name: str = Field(
        description="Имя пользователя",
    )
    last_name: Optional[str] = Field(
        None,
        description="Фамилия пользователя",
    )
    username: Optional[str] = Field(
        None,
        description="Имя пользователя",
    )
    language_code: Optional[LanguageCode] = Field(
        None,
        description="Язык пользователя",
    )
    is_premium: Optional[bool] = Field(
        None,
        description="Является ли пользователь премиум-пользователем",
    )
    added_to_attachment_menu: Optional[bool] = Field(
        None,
        description="Является ли пользователь добавленным в меню вложений",
    )
    can_join_groups: Optional[bool] = Field(
        None,
        description="Может ли пользователь присоединяться к группам",
    )
    can_read_all_group_messages: Optional[bool] = Field(
        None,
        description="Может ли пользователь читать сообщения во всех группах",
    )
    supports_inline_queries: Optional[bool] = Field(
        None,
        description="Поддерживает ли пользователь inline-запросы",
    )
    can_connect_to_business: Optional[bool] = Field(
        None,
        description="Может ли пользователь подключаться к бизнес-соединению",
    )
    has_main_web_app: Optional[bool] = Field(
        None,
        description="Имеет ли пользователь основное веб-приложение",
    )


class MessageEntity(BaseModel):
    type: EntityType = Field(
        description="Тип сущности",
    )
    offset: int = Field(
       description="Начальная позиция сущности в сообщении",
    )
    length: int = Field(
        description="Длина сущности",
    )
    url: Optional[AnyUrl] = Field(
        None,
        description="URL, если сущность является ссылкой",
    )
    user: Optional[User] = Field(
        None,
        description="Пользователь, если сущность является упоминанием",
    )
    language: Optional[str] = Field(
        None,
        description="Язык, если сущность является текстом программирования",
    )
    custom_emoji_id: Optional[str] = Field(
        None,
        description="ID кастомного эмодзи, если сущность является эмодзи",
    )


    @root_validator(pre=False)
    def check_url_type(cls, values):
        if values.get("url") and values.get("type") != EntityType.URL:
            raise ValueError("url must be None if type is not URL")
        return values

    @root_validator(pre=False)
    def check_user_type(cls, values):
        if values.get("user") and values.get("type") != EntityType.TEXT_MENTION:
            raise ValueError("user must be None if type is not TEXT_MENTION")
        return values

    @root_validator(pre=False)
    def check_language_type(cls, values):
        if values.get("language") and values.get("type") != EntityType.PRE:
            raise ValueError("language must be None if type is not PRE")
        return values

    @root_validator(pre=False)
    def check_custom_emoji_type(cls, values):
        if values.get("custom_emoji_id") and values.get("type") != EntityType.CUSTOM_EMOJI:
            raise ValueError("custom_emoji_id must be None if type is not CUSTOM_EMOJI")
        return values


class ReplyParameters(BaseModel):
    message_id : int = Field(
        description="Уникальный идентификатор сообщения",
    )
    chat_id : Optional[int] = Field(
        None,
        description="Уникальный идентификатор чата",
    )
    allow_sending_without_reply : Optional[bool] = Field(
        None,
        description="Разрешить отправку сообщения без ответа",
    )
    quote: Optional[str] = Field(
        None,
        description="Цитируется часть сообщения, на которую нужно ответить; 0-1024 символы после разбора сущностей. "
                    "Цитата должна быть точной подстрокой сообщения, на которое нужно ответить, включая смелые, "
                    "курсивные, подчеркивание, ударные, спойлер и custom_emoji. "
                    "Сообщение не может отправить, если цитата не найдена в исходном сообщении.",
    )
    quote_parse_mode: Optional[str] = Field(
        None,
        description="Режим разбора сущностей в цитате",
    )
    quote_entities: Optional[List[MessageEntity]] = Field(
        None,
        description="Сущности в цитате",
    )
    quote_position: Optional[int] = Field(
        None,
        description="Позиция в цитате",
    )


class WebAppInfo(BaseModel):
    url: AnyHttpUrl = Field(
        description="URL-адрес веб-приложения",
    )


class LoginUrl(BaseModel):
    url: AnyHttpUrl = Field(
        description="URL-адрес веб-приложения",
    )
    forward_text: Optional[str] = Field(
        None,
        description="Текст, который будет отправлен вместо сообщения",
    )
    bot_username: Optional[str] = Field(
        None,
        description="Имя бота, который будет отображаться в качестве отправителя",
    )
    request_write_access: Optional[bool] = Field(
        None,
        description="Запрашивать разрешение на запись",
    )


class SwitchInlineQueryChosenChat(BaseModel):
    query: Optional[str] = Field(
        None,
        description="Запрос, передаваемый в ответ на кнопку",
    )
    allow_user_chats: Optional[bool] = Field(
        None,
        description="Разрешить отправку сообщений в чаты пользователя",
    )
    allow_bot_chats: Optional[bool] = Field(
        None,
        description="Разрешить отправку сообщений в чаты бота",
    )
    allow_group_chats: Optional[bool] = Field(
        None,
        description="Разрешить отправку сообщений в групповые чаты",
    )
    allow_channel_chats: Optional[bool] = Field(
        None,
        description="Разрешить отправку сообщений в каналы",
    )


class CopyTextButton(BaseModel):
    text: str = Field(
        description="Текст кнопки",
    )


class InlineKeyboardButton(BaseModel):
    text: str = Field(
        description="Текст кнопки",
    )
    url: Optional[AnyUrl] = Field(
        None,
        description="URL-адрес, если кнопка является ссылкой",
    )
    callback_data: Optional[str] = Field(
        None,
        description="Данные, передаваемые в ответ на кнопку",
    )
    web_app: Optional[WebAppInfo] = Field(
        None,
        description="Информация о веб-приложении",
    )
    login_url: Optional[LoginUrl] = Field(
        None,
        description="Информация о веб-приложении",
    )
    switch_inline_query: Optional[str] = Field(
        None,
        description="Запрос, передаваемый в ответ на кнопку",
    )
    switch_inline_query_current_chat: Optional[str] = Field(
        None,
        description="Запрос, передаваемый в ответ на кнопку",
    )
    switch_inline_query_chosen_chat: Optional[SwitchInlineQueryChosenChat] = Field(
        None,
        description="Запрос, передаваемый в ответ на кнопку",
    )
    copy_text: Optional[CopyTextButton] = Field(
        None,
        description="Копировать текст кнопки",
    )
    pay: Optional[bool] = Field(
        None,
        description="Разрешить оплату",
    )


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]] = Field(
        description="Массив кнопок",
    )


class KeyboardButtonRequestUsers(BaseModel):
    request_id: int = Field(
        description="Уникальный идентификатор запроса",
    )
    user_is_bot: Optional[bool] = Field(
        None,
        description="Является ли пользователь ботом",
    )
    user_is_premium: Optional[bool] = Field(
        None,
        description="Является ли пользователь премиум-пользователем",
    )
    max_quantity: Optional[int] = Field(
        None,
        description="Максимальное количество пользователей",
    )
    request_name: Optional[bool] = Field(
        None,
        description="Разрешить отправку имени пользователя",
    )
    request_username: Optional[bool] = Field(
        None,
        description="Разрешить отправку имени пользователя",
    )
    request_photo: Optional[bool] = Field(
        None,
        description="Разрешить отправку фото пользователя",
    )

class ChatAdministratorRights(BaseModel):
    """Представляет права администратора в чате."""

    is_anonymous: bool = Field(
        description="Является ли администратор анонимным",
    )
    can_manage_chat: bool = Field(
        description="Может ли администратор управлять чатом",
    )
    can_delete_messages: bool = Field(
        description="Может ли администратор удалять сообщения",
    )
    can_manage_video_chats: bool = Field(
        description="Может ли администратор управлять видео-чатами",
    )
    can_restrict_members: bool = Field(
        description="Может ли администратор ограничивать участников",
    )
    can_promote_members: bool = Field(
        description="Может ли администратор повышать участников",
    )
    can_change_info: bool = Field(
        description="Может ли пользователь изменять информацию о чате",
    )
    can_invite_users: bool = Field(
        description="Может ли пользователь приглашать пользователей",
    )
    can_post_stories: bool = Field(
        description="Может ли администратор публиковать истории",
    )
    can_edit_stories: bool = Field(
        description="Может ли администратор редактировать истории",
    )
    can_delete_stories: bool = Field(
        description="Может ли администратор удалять истории",
    )
    can_post_messages: Optional[bool] = Field(
        description="Может ли администратор отправлять сообщения",
    )
    can_edit_messages: Optional[bool] = Field(
        description="Может ли администратор редактировать сообщения",
    )
    can_pin_messages: Optional[bool] = Field(
        description="Может ли пользователь закреплять сообщения",
    )
    can_manage_topics: Optional[bool] = Field(
        description="Может ли пользователь управлять темами",
    )


class KeyboardButtonRequestChat(BaseModel):
    """Запрос на кнопку клавиатуры чат.

    Этот объект определяет критерии, используемые для запроса подходящего чата.
    Информация о выбранном чате будет передана боту при нажатии соответствующей кнопки.
    Бот будет предоставлена запрашиваемые права в чате, если это необходимо.
    """

    request_id: int = Field(
        description="Уникальный идентификатор запроса",
    )
    chat_is_channel: bool = Field(
        description="Является ли чат каналом",
    )
    chat_is_forum: Optional[bool] = Field(
        None,
        description="Является ли чат форумом",
    )
    chat_has_username: Optional[bool] = Field(
        None,
        description="True, чтобы запросить супергруппу или канал с именем пользователя, передайте False, "
                    "чтобы запросить чат без имени пользователя. "
                    "Если не указано, никаких дополнительных ограничений не применяется.",
    )
    chat_is_created: Optional[bool] = Field(
        None,
        description="True, чтобы запросить чат, принадлежащий пользователю. "
                    "В противном случае, никаких дополнительных ограничений не применяются.",
    )
    user_administrator_rights: Optional[ChatAdministratorRights] = Field(
        None,
        description="Права администратора в чате",
    )
    bot_administrator_rights: Optional[ChatAdministratorRights] = Field(
        None,
        description="Права администратора в чате",
    )
    bot_is_member: Optional[bool] = Field(
        None,
        description="True, чтобы запросить чат с ботом в качестве участника. "
                    "В противном случае, никаких дополнительных ограничений не применяются.",
    )
    request_title: Optional[bool] = Field(
        None,
        description="Разрешить отправку названия чата",
    )
    request_username: Optional[bool] = Field(
        None,
        description="Разрешить отправку имени пользователя",
    )
    request_photo: Optional[bool] = Field(
        None,
        description="Разрешить отправку фото пользователя",
    )


class KeyboardButtonPollType(BaseModel):
    """ Тип опроса

    Этот объект представляет тип опроса, который разрешено создавать и отправлять, когда нажата соответствующая кнопка
    """

    type: str = Field(
        description="Тип опроса",
    )


class KeyboardButton(BaseModel):
    text: str = Field(
        description="Текст кнопки",
    )
    request_user: Optional[KeyboardButtonRequestUsers] = Field(
        None,
        description="Запросить пользователя",
    )
    request_chat: Optional[KeyboardButtonRequestChat] = Field(
        None,
        description="Запросить чат",
    )
    request_contact: Optional[bool] = Field(
        None,
        description="Разрешить отправку контакта",
    )
    request_location: Optional[bool] = Field(
        None,
        description="Разрешить отправку местоположения",
    )
    request_poll: Optional[KeyboardButtonPollType] = Field(
        None,
        description="Запросить опрос",
    )
    web_app: Optional[WebAppInfo] = Field(
        None,
        description="Информация о веб-приложении",
    )


class ReplyKeyboardMarkup(BaseModel):
    keyboard: List[List[KeyboardButton]] = Field(
        description="Массив кнопок",
    )
    resize_keyboard: Optional[bool] = Field(
        None,
        description="Разрешить изменение размера клавиатуры",
    )
    one_time_keyboard: Optional[bool] = Field(
        None,
        description="Разрешить отправку клавиатуры однократно",
    )
    selective: Optional[bool] = Field(
        None,
        description="Разрешить отправку клавиатуры только выбранным пользователям",
    )


class ReplyKeyboardRemove(BaseModel):
    remove_keyboard: bool = Field(
        True,
        description="Удалить клавиатуру",
    )
    selective: Optional[bool] = Field(
        None,
        description="Разрешить отправку клавиатуры только выбранным пользователям",
    )


class ForceReply(BaseModel):
    force_reply: bool = Field(
        True,
        description="Разрешить отправку клавиатуры",
    )
    input_field_placeholder: Optional[str] = Field(
        None,
        description="Текст в поле ввода",
    )
    selective: Optional[bool] = Field(
        None,
        description="Разрешить отправку клавиатуры только выбранным пользователям",
    )


class Chat(BaseModel):
    chat_id: int = Field(
        alias="id",
        description="Уникальный идентификатор чата",
    )
    chat_type: ChatType = Field(
        alias="type",
        description="Тип чата",
    )
    title: Optional[str] = Field(
        None,
        description="Название чата",
    )
    username: Optional[str] = Field(
        None,
        description="Никнейм чата",
    )
    first_name: Optional[str] = Field(
        None,
        description="Имя приватногочата",
    )
    last_name: Optional[str] = Field(
        None,
        description="Фамилия приватного чата",
    )
    is_forum: Optional[bool] = Field(
        None,
        description="Является ли чат форумом",
    )


class Message(BaseModel):
    message_id: int = Field(
        description="Уникальный идентификатор сообщения",
    )
    date: int = Field(
        description="Дата отправки сообщения",
    )
    chat: Chat = Field(
        description="Данные о чате",
    )
    message_from: User = Field(
        alias="from",
        description="Данные о пользователе",
    )
    text: Optional[str] = Field(
        None,
        description="Текст сообщения",
    )


class Update(BaseModel):
    """Входящие обновления.

    В большинстве случаев один из дополнительных параметров может присутствовать в любом данном обновлении.
    """
    update_id: int = Field(
        description="Уникальный идентификатор обновления",
    )
    message: Optional[Message] = Field(
        None,
        description="Данные о сообщении",
    )
    edited_message: Optional[Message] = Field(
        None,
        description="Данные о редактированном сообщении",
    )
    channel_post: Optional[Message] = Field(
        None,
        description="Данные о сообщении в канале",
    )
    edited_channel_post: Optional[Message] = Field(
        None,
        description="Данные о редактированном сообщении в канале",
    )
    # ...