from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from config import BOT_TOKEN, QR_IMAGE, UPI_ID, ADMIN_ID
from database import create_tables, add_user, add_order
from products import PRODUCTS, DURATIONS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Products",
                callback_data="products"
            )
        ],
        [
            InlineKeyboardButton(
                "☎️ Contact Admin",
                url="https://t.me/YOUR_USERNAME"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Join Chan
        "🔥 Welcome to Global Auto Key Store 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Products",
                callback_data="products"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Contact Admin",
                url="https://t.me/YOUR_USERNAME"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url=CHANNEL_URL
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
async def products_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []

    for product in PRODUCTS:
        keyboard.append([
            InlineKeyboardButton(
                product["name"],
                callback_data=f'product_{product["id"]}'
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🔙 Back", callback_data="back")
    ])

    await query.edit_message_text(
        "📦 Select a Product:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
