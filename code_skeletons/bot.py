from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
from price_checker import (
    get_btc_price,
    check_price_changed,
    reset_price,
    show_saved_price,
)

load_dotenv()

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btc_price = ...()

    if btc_price is None:
        await update.message.reply_text("...")
        return

    await update.message.reply_text(f"...")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = ...()
    await update.message.reply_text(...)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...()
    await update.message.reply_text("...")

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = ...()
    await update.message.reply_text(...)

TOKEN = os.getenv("...")
if not TOKEN:
    raise ValueError("...")

app = Application.builder().token(...).build()
app.add_handler(CommandHandler("price", ...))
app.add_handler(CommandHandler("check", ...))
app.add_handler(CommandHandler("reset", ...))
app.add_handler(CommandHandler("show", ...))

app.run_polling()