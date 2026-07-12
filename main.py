import uuid
import logging

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

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    QR_IMAGE,
    UPI_ID,
    CHANNEL_URL,
)

from database import (
    create_tables,
    add_user,
    add_order,
)

from products import (
    PRODUCTS,
    DURATIONS,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

user_orders = {}

create_tables()

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
                "📢 Join Channel",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "👨‍💼 Contact Admin",
                url="https://t.me/premiumsupport_boi"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store 🔥\n\n"
        "Please choose an option below.",
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
                "📢 Join Channel",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "👨‍💼 Contact Admin",
                url="https://t.me/premiumsupport_boi"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store 🔥\n\n"
        "Please choose an option below.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if data == "back_home":
    await start(update, context)
