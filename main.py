import logging
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    QR_IMAGE,
    CHANNEL_URL,
    UPI_ID
)

from database import (
    create_tables,
    add_user,
    add_order
)

from products import (
    PRODUCTS,
    DURATIONS
)


logging.basicConfig(level=logging.INFO)


user_orders = {}


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
        "🔥 Welcome to Nandu Global Key Store 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()


    if query.data == "products":

        buttons = []

        for product in PRODUCTS:
            buttons.append(
                [
                    InlineKeyboardButton(
                        product["name"],
                        callback_data=f"product_{product['id']}"
                    )
                ]
            )

        await query.edit_message_text(
            "🛒 Select Product:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


    elif query.data.startswith("product_"):

        product_id = query.data.replace(
            "product_",
            ""
        )

        user_orders[query.from_user.id] = {
            "product": product_id
        }

        buttons = []

        for duration, price in DURATIONS.items():
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{duration} - ₹{price}",
                        callback_data=f"buy_{duration}"
                    )
                ]
            )

async def admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")

    order_id = parts[1]
    user_id = int(parts[2])

    if query.data.startswith("approve_"):

        await query.message.reply_text(
            "✅ Order Approved"
        )

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Aapka Order Approved ho gaya hai."
        )


    elif query.data.startswith("reject_"):

        await query.message.reply_text(
            "❌ Order Rejected"
        )

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Aapka Order Reject ho gaya hai."
        )
