import os
import uuid

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from products import PRODUCTS, DURATIONS
from keys import KEYS
from config import CHANNEL_URL, UPI_ID, QR_IMAGE
from database import create_tables, add_user, add_order


BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 845178511


user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Products",
                callback_data="products"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url=CHANNEL_URL
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store 🔥\n\nChoose an option:",
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
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="home"
            )
        ])

        await query.edit_message_text(
            "🛒 Select Product:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif data == "home":

        keyboard = [
            [
                InlineKeyboardButton(
                    "📦 Products",
                    callback_data="products"
                )
            ],
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=CHANNEL_URL
                )
            ]
        ]

        await query.edit_message_text(
            "🔥 Welcome to Nandu Global Key Store\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif data.startswith("product_"):

        product_id = data.replace("product_", "")

        keyboard = []

        for duration, price in DURATIONS.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"{duration} - ₹{price}",
                    callback_data=f"buy|{product_id}|{duration}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="products"
            )
        ])

        await query.edit_message_text(
            "⏳ Select Duration:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "home":

        keyboard = [

            [
                InlineKeyboardButton(
                    "🛒 Products",
                    callback_data="products"
                )
            ],

            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=CHANNEL_URL
                )
            ]

        ]


        await query.edit_message_text(

            "🔥 Welcome to Nandu Global Key Store 🔥\n\nChoose an option:",

            reply_markup=InlineKeyboardMarkup(keyboard)

        )



    elif data.startswith("product_"):


        product_id = data.replace(
            "product_",
            ""
        )


        keyboard = []


        for duration, price in DURATIONS.items():

            callback_duration = duration.replace(
                " ",
                "_"
            )


            keyboard.append(

                [

                    InlineKeyboardButton(

                        f"{duration} - ₹{price}",

                        callback_data=f"buy|{product_id}|{callback_duration}"

                    )

                ]

            )


        keyboard.append(

            [

                InlineKeyboardButton(

                    "⬅️ Back",

                    callback_data="products"

                )

            ]

        )


        await query.edit_message_text(

            "⏳ Select Duration:",

            reply_markup=InlineKeyboardMarkup(keyboard)

        )



    elif data.startswith("buy|"):
        # buy वाला code
        pass

    elif data.startswith("approve|"):

        user_id = int(data.split("|")[1])

        info = user_data.get(user_id, {})

        product = info.get("product")

        key = "No Key Available"

        if product in KEYS and KEYS[product]:
            key = KEYS[product].pop(0)

        await context.bot.send_message(
            chat_id=user_id,
            text=f"✅ Payment Approved\n\n🔑 Your Key: {key}"
        )


    elif data.startswith("reject|"):

        user_id = int(data.split("|")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Payment Rejected"
        )


        await query.edit_message_text(
            "❌ Payment Rejected"
        )



if __name__ == "__main__":


    create_tables()


    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    
