from config import BOT_TOKEN, ADMIN_ID, QR_IMAGE, UPI_ID
from database import *
from products import PRODUCTS, DURATIONS

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    keyboard = [
        [InlineKeyboardButton("🛒 Products", callback_data="products")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/YOUR_USERNAME")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/YOUR_CHANNEL")]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Global Auto Key Store 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
