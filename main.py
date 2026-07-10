import os
import uuid

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

from config import *
from products import PRODUCTS, DURATIONS
from database import *

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

create_tables()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username or "",
        user.first_name or ""
    )

    keyboard = [
        [
            InlineKeyboardButton("🛒 Products", callback_data="products")
        ],
        [
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)
        ]
    ]

    text = (
        "🔥 *Welcome to Premium Global Key Store*\n\n"
        "👇 Buy your product from the menu below."
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "products":
        keyboard = []

        for product in PRODUCTS:
            keyboard.append([
                InlineKeyboardButton(
                    product["name"],
                    callback_data=f'product|{product["id"]}'
                )
            ])

        keyboard.append([
            InlineKeyboardButton("⬅ Back", callback_data="back")
        ])

        await query.edit_message_text(
            "🛍 Select Product",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "back":
        keyboard = [
            [
                InlineKeyboardButton("🛒 Products", callback_data="products")
            ],
            [
                InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)
            ]
        ]

        await query.edit_message_text(
            "🔥 Welcome!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("product|"):

        product_id = data.split("|")[1]

        keyboard = []

        for duration, price in DURATIONS.items():
            callback_duration = duration.replace(" ", "_")

            keyboard.append([
                InlineKeyboardButton(
                    f"{duration} - ₹{price}",
                    callback_data=f"buy|{product_id}|{callback_duration}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton("⬅ Back", callback_data="products")
        ])

        await query.edit_message_text(
            "⏳ Select Duration",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("buy|"):

        _, product_id, duration = data.split("|")
        duration = duration.replace("_", " ")

        price = DURATIONS[duration]

        product_name = product_id

        for product in PRODUCTS:
            if product["id"] == product_id:
                product_name = product["name"]
async def receive_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    utr = update.message.text

    info = user_data.get(user.id)

    if not info:
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve|{user.id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject|{user.id}"
            ),
        ]
    ]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🆕 New Order\n\n"
            f"👤 User: {user.first_name}\n"
            f"🆔 User ID: {user.id}\n"
            f"📦 Product: {info['product']}\n"
            f"⏳ Duration: {info['duration']}\n"
            f"💰 Amount: ₹{info['amount']}\n"
            f"🔢 UTR: {utr}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text(
        "✅ UTR received.\nPlease wait for admin approval."
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_utr)
)

print("Bot Started...")
app.run_polling()
