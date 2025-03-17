import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello bhai! Bas mujhe koi photo bhej jisme t.me link ho caption mein, main link ko button bana dunga! 🚀")

# photo handler
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption
    link_pattern = r'(https?://t\.me/[^\s]+|t\.me/[^\s]+)'
    links = re.findall(link_pattern, caption or '')

    if links:
        button_link = links[0]
        caption_text = re.sub(link_pattern, '', caption).strip()  # baaki text rehne do
        keyboard = [
            [InlineKeyboardButton("👉 JOIN HERE 🚀", url=button_link)],
            [InlineKeyboardButton("🔗 Powered by @skillwithgaurav", url="https://t.me/skillwithgaurav")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_photo(
            photo=update.message.photo[-1].file_id,
            caption=f"✨ {caption_text}",
            reply_markup=reply_markup
        )

# error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(r't\.me/'), handle_photo))
app.add_error_handler(error_handler)

if __name__ == '__main__':
    app.run_polling()
