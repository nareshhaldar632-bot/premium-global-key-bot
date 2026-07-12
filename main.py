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
    CHANNEL_URL,
    UPI_ID,
    QR_IMAGE,
)

from database import (
    create_tables,
    add_user,
    add_order,
    update_order_status,
)

from products import (
    PRODUCTS,
    DURATIONS,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

create_tables()

user_orders = {}

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
    CHANNEL_URL,
    UPI_ID,
    QR_IMAGE,
)

from database import (
    create_tables,
    add_user,
    add_order,
    update_order_status,
)

from products import (
    PRODUCTS,
    DURATIONS,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

create_tables()

user_orders = {}

async def products_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []

    for product in PRODUCTS:
        keyboard.append([
            InlineKeyboardButton(
                product["name"],
                callback_data=f"product_{product['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅ Back", callback_data="home")
    ])

    await query.edit_message_text(
        "🛒 Select Product",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def product_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = query.data.replace("product_", "")

    context.user_data["product"] = product_id

    keyboard = []

    for duration, price in DURATIONS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{duration} - ₹{price}",
                callback_data=f"duration_{duration}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅ Back", callback_data="products")
    ])

    await query.edit_message_text(
        "⏳ Select Duration",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def duration_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    duration = query.data.replace("duration_", "")

    product = context.user_data.get("product")

    if not product:
        await query.edit_message_text(
            "❌ Session expired.\n\nPlease use /start again."
        )
        return

    price = DURATIONS[duration]

    order_id = str(uuid.uuid4())[:8].upper()

    context.user_data["order_id"] = order_id
    context.user_data["duration"] = duration
    context.user_data["amount"] = price

    with open(QR_IMAGE, "rb") as photo:

        await query.message.reply_photo(
            photo=photo,
            caption=(
                f"🆔 Order ID : {order_id}\n\n"
                f"📦 Product : {product}\n"
                f"⏳ Duration : {duration}\n"
                f"💰 Amount : ₹{price}\n\n"
                f"UPI ID:\n{UPI_ID}\n\n"
                "✅ Payment karne ke baad apna UTR Number bhejo."
            )
        )

    await query.message.reply_text(
        "✍️ Ab apna UTR Number send karo."
    )
