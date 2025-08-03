import os
import asyncio
from telegram import Bot
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send_message(text: str):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)