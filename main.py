from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import create_tables
from admin import admin_panel

async def start(update, context):
    await update.message.reply_text(
        "👋 Welcome to Nandu Global Key Store!\n\n"
        "Bot is starting successfully."
    )

def main():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
