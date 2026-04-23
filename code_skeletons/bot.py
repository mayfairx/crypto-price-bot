from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
from price_checker import get_coin_price, check_price_change, reset_price, show_saved_price

load_dotenv()

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    coin_price = get_coin_price(symbol)

    if coin_price is None:
        await update.message.reply_text("...")
        return

    await update.message.reply_text(f"{symbol.upper()} price: ${...}")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    result = check_price_change(symbol)
    await update.message.reply_text(...)

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    result = show_saved_price(symbol)
    await update.message.reply_text(...)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    result = reset_price(symbol)
    await update.message.reply_text(...)

async def remove_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "...",
        reply_markup=ReplyKeyboardRemove()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/price btc/eth/sol — show coin price\n"
        "/check btc/eth/sol — check coin price change"
    )

TOKEN = os.getenv("...")
if not TOKEN:
    raise ValueError("...")

app = Application.builder().token(...).build()
app.add_handler(CommandHandler("price", ...))
app.add_handler(CommandHandler("check", ...))
app.add_handler(CommandHandler("show", ...))
app.add_handler(CommandHandler("reset", ...))
app.add_handler(CommandHandler("hide", ...))
app.add_handler(CommandHandler("help", ...))

app.run_polling()