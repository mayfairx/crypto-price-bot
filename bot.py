from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
import json
import time
from price_checker import get_coin_price, check_price_change, reset_price, show_saved_price

load_dotenv()

SUBSCRIPTIONS_FILE = "subscriptions.json"

def read_subscriptions():
    try:
        with open(SUBSCRIPTIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_subscriptions(subscriptions):
    with open(SUBSCRIPTIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(subscriptions, file)

async def check_subscriptions(context: ContextTypes.DEFAULT_TYPE):
    subscriptions = read_subscriptions()
    current_time = time.time()

    for chat_id, coins in subscriptions.items():
        for symbol, data in coins.items():
            interval = data["interval"] * 60 
            last_check = data["last_check"]

            if current_time - last_check < interval:
                continue
            
            result = check_price_change(symbol)

            subscriptions[chat_id][symbol]["last_check"] = current_time

            if "No changes." not in result:
                await context.bot.send_message(chat_id=int(chat_id), text=result)

    write_subscriptions(subscriptions)


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
        "/check btc/eth/sol — check coin price change\n"
        "/track btc 1 — subscribe to price updates every 1 minute\n"
        "/untrack btc — stop tracking coin"
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat id: {update.effective_chat.id}")

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Use: /track btc 5")
        return
    
    symbol = context.args[0].lower()
    interval = context.args[1]

    if not interval.isdigit():
        await update.message.reply_text("Interval must be a number. Example: /track btc 5")
        return
    
    interval = int(interval)

    subscriptions = read_subscriptions()
    chat_id = str(update.effective_chat.id)

    if chat_id not in subscriptions:
        subscriptions[chat_id] = {}

    subscriptions[chat_id][symbol] = {
        "interval": interval,
        "last_check": 0
    }

    write_subscriptions(subscriptions)

    await update.message.reply_text(f"Tracking {symbol.upper()} every {interval} minutes.")    

async def untrack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Use: /untrack btc")
        return
    
    symbol = context.args[0].lower()
    chat_id = str(update.effective_chat.id)

    subscriptions = read_subscriptions()

    if chat_id not in subscriptions or symbol not in subscriptions[chat_id]:
        await update.message.reply_text(f"You are not tracking {symbol.upper()}.")
        return
    
    del subscriptions[chat_id][symbol]

    if not subscriptions[chat_id]:
        del subscriptions[chat_id]

    write_subscriptions(subscriptions)

    await update.message.reply_text(f"Stopped tracking {symbol.upper()}.")

async def list_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    subscriptions = read_subscriptions()

    if chat_id not in subscriptions or not subscriptions[chat_id]:
        await update.message.reply_text("You are not tracking anything.")
        return
    
    message = "You are tracking:\n"

    for symbol, data in subscriptions[chat_id].items():
        interval = data["interval"]
        message += f"{symbol.upper()} — every {interval} min\n"

    await update.message.reply_text(message)

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
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("track", track))
app.add_handler(CommandHandler("untrack", untrack))
app.add_handler(CommandHandler("list", list_tracking))

app.job_queue.run_repeating(check_subscriptions, interval=30, first=5)

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

threading.Thread(target=run_server).start()

app.run_polling()

