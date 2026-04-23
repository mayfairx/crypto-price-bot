from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

import os
from price_checker import get_coin_price, check_price_change, reset_price, show_saved_price

load_dotenv()

price_job = None

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

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat id: {update.effective_chat.id}")

async def send_price_update(context: ContextTypes.DEFAULT_TYPE):
    chat_id = 1854986874
    result = check_price_change("btc")
    
    if "No changes." in result:
        return

    await context.bot.send_message(chat_id=chat_id, text=result)

async def track_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global price_job

    if price_job is not None:
        await update.message.reply_text("Auto-tracking is already on.")
        return
    
    price_job = context.job_queue.run_repeating(
        send_price_update,
        interval=30,
        first=5
    )

    await update.message.reply_text("Auto-tracking started.")

async def track_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global price_job

    if price_job is None:
        await update.message.reply_text("Auto-tracking is already off.")
        return
    
    price_job.schedule_removal()
    price_job = None

    await update.message.reply_text("Auto-tracking stopped.")

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
app.add_handler(CommandHandler("track_on", track_on))
app.add_handler(CommandHandler("track_off", track_off))

app.run_polling()