import os
from config import CHANNEL_URL, UPI_ID, QR_IMAGE
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from database import create_tables, add_user
from products import PRODUCTS, DURATIONS

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(user.id, user.username, user.first_name)

    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
    ]

    await update.message.reply_text(
        "👋 Welcome to Nandu Global Key Store\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # Products
    if data == "products":
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
            "📦 Select Product",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Home
    elif data == "home":
        keyboard = [
            [InlineKeyboardButton("📦 Products", callback_data="products")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
        ]

        await query.message.reply_photo(
    photo=open("qr.jpg", "rb"),
    caption=(
        f"💳 Payment Details\n\n"
        f"📦 Product: {product}\n"
        f"⌛ Duration: {duration}\n"
        f"💰 Price: ₹{price}\n"
        f"🆔 UPI ID: {UPI_ID}\n\n"
        "QR Scan karke payment kare.\n"
        "Payment ke baad UTR number bheje."
    )
        )

    # Product Selected
    elif data.startswith("product_"):
        product_id = data.replace("product_", "")

        keyboard = []

        for duration, price in DURATIONS.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"{duration} - ₹{price}",
                    callback_data=f"buy_{product_id}_{duration}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton("⬅ Back", callback_data="products")
        ])

        await query.edit_message_text(
            "⏳ Select Duration",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Buy
    elif data.startswith("buy_"):
    parts = data.split("_")

    product = parts[1]
    duration = "_".join(parts[2:])

    price = DURATIONS.get(duration, 0)

    await query.message.reply_photo(
        photo=open(QR_IMAGE, "rb"),
        caption=(
            f"💳 Payment Details\n\n"
            f"📦 Product: {product}\n"
            f"⏳ Duration: {duration}\n"
            f"💰 Price: ₹{price}\n"
            f"🆔 UPI ID: {UPI_ID}\n\n"
            "📷 QR Scan karke payment kare.\n"
            "Payment ke baad UTR number bheje."
        )
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    create_tables()

    app.run_polling()


if __name__ == "__main__":
    main()
