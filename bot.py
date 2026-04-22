from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
from price_checker import get_btc_price, check_price_change, reset_price, show_saved_price

load_dotenv()

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btc_price = get_btc_price()

    if btc_price is None:
        await update.message.reply_text("Could not get BTC price from API.")
        return

    await update.message.reply_text(f"BTC Price: ${btc_price}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = check_price_change()
    await update.message.reply_text(result)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_price()
    await update.message.reply_text("Price reset. state.txt cleared.")

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = show_saved_price()
    await update.message.reply_text(result)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("show", show))

app.run_polling()
