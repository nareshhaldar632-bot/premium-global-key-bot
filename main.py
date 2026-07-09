import os
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from products import PRODUCTS, DURATIONS
from keys import KEYS

from config import CHANNEL_URL, UPI_ID, QR_IMAGE

from database import create_tables, add_user, add_order


BOT_TOKEN = os.getenv("BOT_TOKEN")

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

            keyboard.append(
                [
                    InlineKeyboardButton(
                        product["name"],
                        callback_data=f"product_{product['id']}"
                    )
                ]
            )

        keyboard.append(
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        )

        await query.edit_message_text(
            "🛒 Select Product",
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

        await
query.edit_message_text(
            "🔥 Welcome to Nandu
Global Key Store\n\nChoose an option:",
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
                "⬅ Back",
                callback_data="products"
            )
        ]
    )

    await query.edit_message_text(
        "⏳ Select Duration",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
elif data.startswith("buy|"):

        _, product_id, duration = data.split("|")


        duration = duration.replace(
            "_",
            " "
        )


        price = DURATIONS.get(
            duration,
            0
        )


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


    elif data.startswith("approve|"):

        user_id = int(
            data.split("|")[1]
        )


        info = user_data.get(
            user_id,
            {}
        )


        product = info.get(
            "product"
        )


        key = "No Key Available"


        if product in KEYS and KEYS[product]:

            key = KEYS[product].pop(0)


        await context.bot.send_message(

            chat_id=user_id,

            text=(

                "✅ Payment Approved!\n\n"

                f"🔑 Your Key:\n{key}\n\n"

                "Thank you for using Nandu Global Key Store."

            )

        )


        await query.edit_message_text(
            "✅ Payment Approved"
        )
            elif data.startswith("reject|"):

        user_id = int(
            data.split("|")[1]
        )


        await context.bot.send_message(

            chat_id=user_id,

            text=(
                "❌ Payment Rejected.\n\n"
                "Please contact admin."
            )

        )


        await query.edit_message_text(
            "❌ Payment Rejected"
        )



async def receive_utr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    utr = update.message.text


    info = user_data.get(user.id)


    if not info:
        return



    keyboard = [

        [

            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve|{user.id}"
            ),

            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject|{user.id}"
            )

        ]

    ]



    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=(

            "💳 New Payment\n\n"

            f"👤 User: {user.first_name}\n"
            f"🆔 ID: {user.id}\n"
            f"📦 Product: {info['product']}\n"
            f"⏳ Duration: {info['duration']}\n"
            f"💰 Amount: ₹{info['amount']}\n"
            f"🔢 UTR: {utr}"

        ),

        reply_markup=InlineKeyboardMarkup(keyboard)

    )



    await update.message.reply_text(

        "✅ Payment submitted.\nPlease wait for approval."

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


    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_utr
        )
    )


    print("Bot Started...")


    app.run_polling()
