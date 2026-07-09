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


        product_id = data.replace(
            "product_",
            ""
        )


        keyboard = []


        for duration, price in DURATIONS.items():

            callback = duration.replace(
                " ",
                "_"
            )


            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{duration} - ₹{price}",
                        callback_data=f"buy|{product_id}|{callback}"
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


        product_id = data.replace(
            "product_",
            ""
        )


        keyboard = []


        for duration, price in DURATIONS.items():

            callback = duration.replace(
                " ",
                "_"
            )


            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{duration} - ₹{price}",
                        callback_data=f"buy|{product_id}|{callback}"
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
