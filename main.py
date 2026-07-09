import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import CHANNEL_URL, UPI_ID, QR_IMAGE
from database import (
    create_tables,
    add_user,
    add_order,
)
from products import PRODUCTS, DURATIONS

BOT_TOKEN = os.getenv("BOT_TOKEN")
import uuid
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
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)]
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
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "home":

        keyboard = [
            [InlineKeyboardButton("📦 Products", callback_data="products")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)]
        ]

        await query.edit_message_text(
            "🔥 Welcome to Nandu Global Key Store\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("product_"):

        product_id = data.replace("product_", "")

        keyboard = []

        for duration, price in DURATIONS.items():
            callback = duration.replace(" ", "_")

            keyboard.append([
                InlineKeyboardButton(
                    f"{duration} - ₹{price}",
                    callback_data=f"buy|{product_id}|{callback}"
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

        price = DURATIONS.get(duration, 0)
        order_id = str(uuid.uuid4())[:8]

        product_name = product_id

        for product in PRODUCTS:
            if product["id"] == product_id:
                product_name = product["name"]
                break

        user_data[query.from_user.id] = {
            "order_id": order_id,
            "product": product_name,
            "duration": duration,
            "amount": price
        }

        add_order(
            order_id,
            query.from_user.id,
            product_name,
            duration,
            price,
            ""
        )

        await query.message.reply_photo(
            photo=open(QR_IMAGE, "rb"),
            caption=(
                "💳 Payment Details\n\n"
                f"📦 Product: {product_name}\n"
                f"⏳ Duration: {duration}\n"
                f"💰 Price: ₹{price}\n"
                f"🆔 UPI ID: {UPI_ID}\n\n"
                "📷 QR Scan karke payment kare.\n"
                "✅ Payment ke baad UTR number bheje."
            )
        )
async def receive_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    utr = update.message.text

    info = user_data.get(user.id)

    if not info:
        return

    keyboard = [[
        InlineKeyboardButton(
            "✅ Approve",
            callback_data=f"approve|{user.id}"
        ),
        InlineKeyboardButton(
            "❌ Reject",
            callback_data=f"reject|{user.id}"
        )
    ]]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"💳 New Payment\n\n"
            f"👤 {user.first_name}\n"
            f"🆔 {user.id}\n"
            f"📦 {info['product']}\n"
            f"⏳ {info['duration']}\n"
            f"💰 ₹{info['amount']}\n"
            f"UTR: {utr}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text(
        "✅ Payment submitted.\nPlease wait for admin approval."
    )
if __name__ == "__main__":
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        receive_utr
    )
    )

    print("Bot started...")

    app.run_polling()
