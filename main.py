import os
import time
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

from database import (
    create_tables,
    add_user,
    add_order,
    update_order_status,
    get_order,
)

from products import PRODUCTS, DURATIONS
from config import ADMIN_ID, QR_IMAGE

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
        [
            InlineKeyboardButton(
                "📞 Contact Admin",
                url="https://t.me/YOUR_USERNAME"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url="https://t.me/YOUR_CHANNEL"
            )
        ],
    ]

    await update.message.reply_text(
        "👋 Welcome to Nandu Global Key Store\n\nChoose an option:",
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
    product_id = query.data.replace("product_", "")
    context.user_data["product"] = product_id

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
        duration = query.data.replace("buy_", "")
        product = context.user_data.get("product")

        context.user_data["duration"] = duration
        context.user_data["amount"] = DURATIONS[duration]

        await query.message.reply_photo(
            photo=open(QR_IMAGE, "rb"),
            caption=(
                f"💳 Payment Details\n\n"
                f"📦 Product: {product}\n"
                f"⏳ Duration: {duration}\n"
                f"💰 Amount: ₹{DURATIONS[duration]}\n\n"
                "✅ Payment karne ke baad UTR Number bhej do."
            ),
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

    product = context.user_data.get("product", "Unknown")
    duration = context.user_data.get("duration", "Unknown")
    amount = context.user_data.get("amount", 0)

    order_id = str(int(time.time()))

    add_order(
        order_id,
        update.effective_user.id,
        product,
        duration,
        amount,
        utr_number,
    )

    keyboard = [[
        InlineKeyboardButton(
            "✅ Approve",
            callback_data=f"approve_{order_id}"
        ),
        InlineKeyboardButton(
            "❌ Reject",
            callback_data=f"reject_{order_id}"
        ),
    ]]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🆕 New Order\n\n"
            f"🆔 Order ID: {order_id}\n"
            f"👤 User: {update.effective_user.id}\n"
            f"📦 Product: {product}\n"
            f"⏳ Duration: {duration}\n"
            f"💰 Amount: ₹{amount}\n"
            f"💳 UTR: {utr_number}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

    await update.message.reply_text(
        "✅ UTR Received.\n\nAdmin payment verify karega."
    )


    elif query.data.startswith("approve_"):
        order_id = query.data.replace("approve_", "")

        update_order_status(order_id, "APPROVED")

        order = get_order(order_id)
        user_id = order[2]

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Payment Approved!\n\nAdmin jaldi aapki key bhejega."
        )

        await query.edit_message_text("✅ Order Approved")


    elif query.data.startswith("reject_"):
        order_id = query.data.replace("reject_", "")

        update_order_status(order_id, "
                            
