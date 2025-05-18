import uvicorn
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.params import Depends

from bot.bot_type import Update
from bot.handlers import update_handler
from bot.client import TelegramClient
from config import Settings, settings

app = FastAPI()

def authorize_webhook(
    x_telegram_bot_api_secret_token: str = Header(..., alias="X-Telegram-Bot-Api-Secret-Token")
) -> str:
    if x_telegram_bot_api_secret_token != settings.SECRET_TOKEN.get_secret_value():
        raise HTTPException(status_code=403, detail="Forbidden")
    return x_telegram_bot_api_secret_token

@app.post("/webhook/")
async def telegram_webhook(update: Update,tg_token: str = Depends(authorize_webhook)):
    await update_handler(update, TelegramClient(settings.BOT_TOKEN.get_secret_value()))
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=False,
    )
