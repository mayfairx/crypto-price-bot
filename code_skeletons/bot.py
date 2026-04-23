from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
from price_checker import get_coin_price, check_price_change, reset_price, show_saved_price

load_dotenv()

price_job = None

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

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    result = reset_price(symbol)
    await update.message.reply_text(...)

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    result = show_saved_price(symbol)
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

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat id: {...}")

async def send_price_update(context: ContextTypes.DEFAULT_TYPE):
    chat_id = ...
    result = check_price_change("...")

    if "No changes." in result:
        return

    await context.bot.send_message(chat_id=chat_id, text=result)

async def track_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global price_job

    if price_job is not None:
        await update.message.reply_text("...")
        return

    price_job = context.job_queue.run_repeating(
        send_price_update,
        interval=...,
        first=...
    )

    await update.message.reply_text("...")

async def track_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global price_job

    if price_job is None:
        await update.message.reply_text("...")
        return

    price_job.schedule_removal()
    price_job = None

    await update.message.reply_text("...")

TOKEN = os.getenv("...")
if not TOKEN:
    raise ValueError("...")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("show", show))
app.add_handler(CommandHandler("hide", remove_keyboard))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("track_on", track_on))
app.add_handler(CommandHandler("track_off", track_off))

app.run_polling()