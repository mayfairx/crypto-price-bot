from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
import json
import time

from price_checker import get_coin_price, check_price_change, reset_price, show_saved_price

load_dotenv()

SUBSCRIPTIONS_FILE = "..."

def read_subscriptions():
    try:
        with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_subscriptions(subscriptions):
    with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(..., file)

async def check_subscriptions(context: ContextTypes.DEFAULT_TYPE):
    subscriptions = read_subscriptions()
    current_time = time.time()

    for chat_id, coins in subscriptions.items():
        for symbol, data in coins.items():
            interval = data["..."] * 60
            last_check = data["..."]

            if current_time - last_check < interval:
                continue

            result = check_price_change(...)

            subscriptions[chat_id][symbol]["..."] = current_time

            if "No changes." not in result:
                await context.bot.send_message(
                    chat_id=int(...),
                    text=...
                )

    write_subscriptions(subscriptions)

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
        "/check btc/eth/sol — check coin price change\n"
        "/track btc 1 — subscribe to price updates every 1 minute\n"
        "/untrack btc — stop tracking coin"
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat id: {...}")

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    interval = context.args[1]

    if not interval.isdigit():
        await update.message.reply_text("...")
        return

    interval = int(interval)

    subscriptions = read_subscriptions()
    chat_id = str(update.effective_chat.id)

    if chat_id not in subscriptions:
        subscriptions[chat_id] = {}

    subscriptions[chat_id][symbol] = {
        "interval": ...,
        "last_check": ...
    }

    write_subscriptions(subscriptions)

    await update.message.reply_text(
        f"Tracking {symbol.upper()} every {interval} minutes."
    )

async def untrack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("...")
        return

    symbol = context.args[0].lower()
    chat_id = str(update.effective_chat.id)

    subscriptions = read_subscriptions()

    if chat_id not in subscriptions or symbol not in subscriptions[chat_id]:
        await update.message.reply_text(...)
        return

    del subscriptions[chat_id][symbol]

    if not subscriptions[chat_id]:
        del subscriptions[chat_id]

    write_subscriptions(subscriptions)

    await update.message.reply_text(f"Stopped tracking {symbol.upper()}.")

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
app.add_handler(CommandHandler("track", track))
app.add_handler(CommandHandler("untrack", untrack))

app.job_queue.run_repeating(check_subscriptions, interval=30, first=5)

app.run_polling()