import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from database import create_tables, add_user
from products import PRODUCTS, DURATIONS
from config import CHANNEL_URL

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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "products":
   0     keyboard = []

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

        await query.edit_message_text(
            f"💳 Payment Details\n\n"
            f"Product: {product_id}\n"
            f"Duration: {duration}\n"
            f"Amount: ₹{price}\n\n"
            "Payment karne ke baad UTR number bheje."
        )
def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
