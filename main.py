import os
import uuid

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from products import PRODUCTS, DURATIONS
from keys import KEYS
from config import CHANNEL_URL, UPI_ID, QR_IMAGE
from database import create_tables, add_user, add_order

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8469175911

user_data = {}


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
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "products":

        keyboard = []

        for product in PRODUCTS:

            keyboard.append(
                [
                    InlineKeyboardButton(
                        product["name"],
                        callback_data=f"product_{product['id']}"
                    )
                ]
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        )

        await query.edit_message_text(
            "🛒 Select Product",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "home":

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
            ]
        ]

        await query.edit_message_text(
            "🔥 Welcome to Nandu Global Key Store\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
                )
