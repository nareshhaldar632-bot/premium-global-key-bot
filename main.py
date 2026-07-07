import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from products import PRODUCTS, DURATIONS
from config import ADMIN_ID, QR_IMAGE

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Premium_Mods_Reseller")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/primesupport_boi")],
    ]

    await update.message.reply_text(
        "👋 Welcome to Premium Global Store\n\nChoose an option:",
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

        keyboard.append([
            InlineKeyboardButton("⬅️ Back", callback_data="back")
        ])

        await query.edit_message_text(
            "📦 Select Product",
            reply_markup=InlineKeyboardMarkup(keyboard)
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
            InlineKeyboardButton("⬅️ Back", callback_data="products")
        ])

        await query.edit_message_text(
            "⏳ Select Duration",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data.startswith("buy_"):

    await query.message.reply_photo(
    photo=QR_IMAGE,
    caption="💳 Payment करें\n\nPayment के बाद अपना UTR Number भेजें।\n\nExample: 123456789012"
    )
  


    elif query.data == "back":

        keyboard = [
            [InlineKeyboardButton("📦 Products", callback_data="products")]
        ]

        await query.edit_message_text(
            "👋 Welcome Back",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def utr(update, context):
    utr_number = update.message.text

    await update.message.reply_text(
        "✅ UTR Received\nAdmin payment verify karega."
    )
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, utr))
print("Bot Started...")
app.run_polling()
