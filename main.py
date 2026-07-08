import os
from admin import admin_panel
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from database import create_tables, add_user, add_order
from config import CHANNEL_URL, QR_IMAGE, ADMIN_ID
from products import PRODUCTS, DURATIONS

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name,
    )

    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
    ]

    await update.message.reply_text(
        "👋 Welcome to Nandu Global Key Store\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


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

        await query.edit_message_text(
            "📦 Select Product",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("product_"):
        product_id = query.data.replace("product_", "")

        keyboard = []

        for duration, price in DURATIONS.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"{duration} - ₹{price}",
                    callback_data=f"buy_{product_id}_{duration}"
                )
            ])

        await query.edit_message_text(
            "⏳ Select Duration",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("buy_"):
        data = query.data.replace("buy_", "")
        product_id, duration = data.split("_")

        price = DURATIONS[duration]

        await query.message.reply_photo(
    photo=open(QR_IMAGE, "rb"),
    caption=(
        f"💳 Payment Details\n\n"
        f"📦 Product: {product_id}\n"
        f"⏳ Duration: {duration}\n"
        f"💰 Amount: ₹{price}\n\n"
        f"🏦 UPI ID:\n7425974582@ibl\n\n"
        "📷 QR Scan karke payment kare.\n\n"
        "Payment ke baad apna UTR Number bheje."
    )
        )
