import os
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import (
    create_tables,
    add_user,
    add_order,
    update_order_status,
    get_order,
)

from products import PRODUCTS, DURATIONS
from config import ADMIN_ID, QR_IMAGE

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(
        update.effective_user.id,
        update.effective_user.username,
        update.effective_user.first_name,
    )

    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/YOUR_USERNAME")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/YOUR_CHANNEL")],
    ]

    await update.message.reply_text(
        "👋 Welcome to Premium Global Store\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "products":
        keyboard = []

        for product in PRODUCTS:
            keyboard.append([
                InlineKeyboardButton(
                    product["name"],
                    callback_data=f"product_{product['id']}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton("⬅ Back", callback_data="back")
        ])

        await query.edit_message_text(
            "📦 Select Product",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
