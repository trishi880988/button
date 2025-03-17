import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

link_regex = r'(https?://[^\s]+)'

@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message):
    if message.caption:
        links = re.findall(link_regex, message.caption)
        if links:
            keyboard = InlineKeyboardMarkup()
            for idx, link in enumerate(links):
                keyboard.add(InlineKeyboardButton(text=f"Open Link {idx+1}", url=link))
            await message.reply_photo(message.photo[-1].file_id, caption="Link extracted from caption!", reply_markup=keyboard)
        else:
            await message.reply("No link found in the caption.")
    else:
        await message.reply("No caption found in the photo.")

@dp.message_handler(CommandStart())
async def start_handler(message: types.Message):
    await message.reply("👋 Welcome! Send me a photo with a link in the caption and I'll turn the link into a button!")

if __name__ == "__main__":
    executor.start_polling(dp)
