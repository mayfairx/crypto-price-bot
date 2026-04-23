from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
from price_checker import get_coin_price, check_price_change, reset_price, show_saved_price

load_dotenv()

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /price btc or /price eth or /price sol")
        return
    
    symbol = context.args[0].lower()
    coin_price = get_coin_price(symbol)

    if coin_price is None:
        await update.message.reply_text("Unknown coin or API error.")
        return
    
    await update.message.reply_text(f"{symbol.upper()} price: ${coin_price}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = check_price_change("btc")
    await update.message.reply_text(result)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_price()
    await update.message.reply_text("Saved BTC price reset.")

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
