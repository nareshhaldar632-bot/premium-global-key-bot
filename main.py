import os
from database import add_order
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import time
from database import create_tables, add_user
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from products import PRODUCTS, DURATIONS
from config import ADMIN_ID, QR_IMAGE

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Premium_Mods_Reseller")],
        [InlineKeyboardButton("🎭 Join Channel", url="https://t.me/primesupport_boi")],
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

    
    elif query.data.startswith("product_"):
        keyboard = []

        for day, price in DURATIONS.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"{day} - ₹{price}",
                    callback_data=f"buy_{day}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton("⬅ Back", callback_data="products")
        ])

        await query.edit_message_text(
            "⏳ Select Duration",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    elif query.data.startswith("buy_"):
        await query.message.reply_photo(
            photo=open(QR_IMAGE, "rb"),
            caption=(
                "💳 Payment करें\n\n"
                "Payment के बाद अपना UTR Number भेजें।\n\n"
                "Example: 123456789012"
            ),
        )
    elif query.data.startswith("approve_"):
        order_id = query.data.replace("approve_", "")

        await query.edit_message_text(
            f"✅ Order {order_id} Approved"
        )

    elif query.data.startswith("reject_"):
        order_id = query.data.replace("reject_", "")

        await query.edit_message_text(
            f"❌ Order {order_id} Rejected"
        )
   elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📦 Products", callback_data="products")]
        ]

        await query.edit_message_text(
            "👋 Welcome Back",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


async def utr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utr_number = update.message.text

    order_id = str(int(time.time()))

    add_order(
        order_id,
        update.effective_user.id,
        "Unknown",
        "Unknown",
        0,
        utr_number
    )

    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{order_id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{order_id}")
    ]]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🛒 New Order\n\n"
            f"Order ID: {order_id}\n"
            f"User: {update.effective_user.id}\n"
            f"UTR: {utr_number}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text(
        "✅ UTR Received.\n\nAdmin payment verify karega."
    )


def main():
    from database import create_tables
    create_tables()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, utr)
    )

    print("Bot Started...")
    app.run_polling()


if __name__ == "__main__":
    main()
