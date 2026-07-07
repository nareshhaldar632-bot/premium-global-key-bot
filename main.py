import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from products import PRODUCTS

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Products", callback_data="products")],
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Premium_Mods_Reseller")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/primesupport_boi")],
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
    keyboard.append(
        [
            InlineKeyboardButton(
                product["name"],
                callback_data=f"product_{product['id']}"
            )
        ]
    )

        keyboard.append(
            [InlineKeyboardButton("⬅️ Back", callback_data="back")]
        )

        await query.edit_message_text(
            "📦 Select a Product",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
elif query.data.startswith("product_"):
    product_id = query.data.replace("product_", "")

    keyboard = [
        [InlineKeyboardButton("1 Day - ₹60", callback_data="coming_soon")],
        [InlineKeyboardButton("3 Days - ₹100", callback_data="coming_soon")],
        [InlineKeyboardButton("7 Days - ₹150", callback_data="coming_soon")],
        [InlineKeyboardButton("10 Days - ₹190", callback_data="coming_soon")],
        [InlineKeyboardButton("15 Days - ₹300", callback_data="coming_soon")],
        [InlineKeyboardButton("30 Days - ₹500", callback_data="coming_soon")],
        [InlineKeyboardButton("⬅️ Back", callback_data="products")],
    ]

    await query.edit_message_text(
        "⏳ Select Duration",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📦 Products", callback_data="products")],
            [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Premium_Mods_Reseller")],
            [InlineKeyboardButton("📢 Join Channel", url="https://t.me/primesupport_boi")],
        ]

        await query.edit_message_text(
            "👋 Welcome to Premium Global Store\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    else:
        await query.answer("Coming Soon!", show_alert=True)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Started...")
app.run_polling()
