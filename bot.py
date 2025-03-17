import os
import re
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

styles = [
    ["🔥", "🚀", "⚡", "🎯", "🌈"],
    ["💎", "✨", "🎉", "🟢", "🔵"],
    ["💥", "🧨", "🌟", "🪐", "🎁"],
    ["🥇", "🏆", "🎖️", "🎯", "🎇"],
    ["👑", "💫", "🔮", "🧿", "🌀"]
]

link_pattern = r'(https?://\S+|t\.me/\S+)'

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo_with_link(message: types.Message):
    if message.caption:
        links = re.findall(link_pattern, message.caption)
        text_without_links = re.sub(link_pattern, '', message.caption).strip()
        
        if links:
            style_pack = random.choice(styles)
            keyboard = InlineKeyboardMarkup(row_width=1)
            for idx, link in enumerate(links, start=1):
                left = random.choice(style_pack)
                right = random.choice(style_pack)
                button_text = f"{left} Visit Link {idx} {right}"
                button_url = link if link.startswith('http') else f"https://{link}"
                keyboard.add(InlineKeyboardButton(button_text, url=button_url))
            
            final_caption = f"{text_without_links}\n\n🚀 Powered by @skillwithgaurav"
            await message.reply_photo(
                message.photo[-1].file_id,
                caption=final_caption,
                reply_markup=keyboard
            )

if __name__ == "__main__":
    executor.start_polling(dp)

