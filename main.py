import uuid
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
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
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
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
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
        [InlineKeyboardButton("👨‍💼 Contact Admin", url="https://t.me/premiumsupport_boi")]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store 🔥\n\n"
        "Please choose an option below.",
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
                callback_data=f"product_{product['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("⬅ Back", callback_data="home")
    ])async def product_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = query.data.replace("product_", "")

    user_orders[query.from_user.id] = {
        "product": product_id
    }

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
        "📅 Select Duration",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def duration_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    duration = query.data.replace("duration_", "")

    order = user_orders.get(query.from_user.id)

    if not order:
        await query.message.reply_text("❌ Session expired. Please /start again.")
        return

    order["duration"] = duration
    order["price"] = DURATIONS[duration]

    with open(QR_IMAGE, "rb") as photo:
        await query.message.reply_photo(
            photo=photo,
            caption=(
                f"💳 Payment Amount: ₹{order['price']}\n\n"
                f"UPI ID:\n{UPI_ID}\n\n"
                "Payment complete karke apna UTR Number bhejo."
            )
        )

    await query.message.reply_text("✍️ UTR Number send karo.")

    

    await query.edit_message_text(
        "🛒 Select Product",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



create_tables()

user_orders = {}
