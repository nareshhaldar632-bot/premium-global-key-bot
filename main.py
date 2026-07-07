import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Premium_Mods_Reseller")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/primesupport_boi")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\nChoose an option below:",
        reply_markup=reply_markup
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot Started...")
app.run_polling()
