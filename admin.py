from telegram import Update
from telegram.ext import ContextTypes

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👨‍💼 Admin Panel\n\n"
        "Commands:\n"
        "/orders - View Orders\n"
        "/users - Total Users\n"
        "/broadcast - Broadcast Message"
    )
