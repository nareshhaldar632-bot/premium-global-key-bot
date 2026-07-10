import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "products":
        await query.edit_message_text(
            "🛒 Products List\n\n"
            "• APK MC PANEL\n"
            "• BR MOD\n"
            "• DRIPCLIENT\n"
            "• KOS\n"
            "• NEO STRIKE"
        )
    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Products",
                callback_data="products"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Premium Global Key Store",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Started...")
app.run_polling()
