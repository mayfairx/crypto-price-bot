from telegram import Update, ReplyKeyboardRemove
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
    if not context.args:
        await update.message.reply_text("Use /check btc or /check eth or /check sol")
        return
    
    symbol = context.args[0].lower()
    result = check_price_change(symbol)
    await update.message.reply_text(result)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use /reset btc or /reset eth or /reset sol")
        return
    
    symbol = context.args[0].lower()
    result = reset_price(symbol)
    await update.message.reply_text(result)

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use /show btc or /show eth or /show sol")
        return
    
    symbol = context.args[0].lower()
    result = show_saved_price(symbol)
    await update.message.reply_text(result)

async def remove_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Keyboard removed.",
        reply_markup=ReplyKeyboardRemove()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/price btc/eth/sol — show coin price\n"
        "/check btc/eth/sol — check coin price change"
    )

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found in .env")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("show", show))
app.add_handler(CommandHandler("hide", remove_keyboard))
app.add_handler(CommandHandler("help", help_command))

app.run_polling()