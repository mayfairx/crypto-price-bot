# Crypto Price Bot

A simple Telegram bot built with Python that tracks cryptocurrency prices in real time using the CoinGecko API.

## Features

- `/price <coin>` — show current price
- `/check <coin>` — check price change
- `/show <coin>` — show saved price
- `/reset <coin>` — reset saved price
- `/track <coin> <minutes>` — subscribe to price updates
- `/untrack <coin>` — stop tracking coin
- `/list` — show active subscriptions
- `/start` — quick start guide
- `/help` — show commands
- `/hide` — remove keyboard

## Supported Coins

- `btc`
- `eth`
- `sol`

## Project Structure

- `bot.py` — Telegram bot logic
- `price_checker.py` — API and price logic
- `state.json` — saved coin prices (ignored)
- `subscriptions.json` — user subscriptions (ignored)
- `requirements.txt` — dependencies
- `.env` — bot token (not uploaded)
- `.gitignore` — ignored files

## Installation

```bash
pip install -r requirements.txt
```

## Setup & Run

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
```

Run the bot:

```bash
python bot.py
```

## Notes

- Uses CoinGecko API
- Supports BTC, ETH and SOL
- Price updates are checked every 30 seconds
- Subscriptions are stored in `subscriptions.json`
- Prices are stored in `state.json`
- Uses `python-telegram-bot[job-queue]`