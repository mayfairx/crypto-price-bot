# Crypto Price Bot

A simple Telegram bot built with Python that gets crypto prices from the CoinGecko API.

## Features
- `/price btc` — show BTC price
- `/price eth` — show ETH price
- `/price sol` — show SOL price

- `/check btc` — check BTC price change
- `/check eth` — check ETH price change
- `/check sol` — check SOL price change

- `/show btc` — show saved BTC price
- `/show eth` — show saved ETH price
- `/show sol` — show saved SOL price

- `/reset btc` — reset saved BTC price
- `/reset eth` — reset saved ETH price
- `/reset sol` — reset saved SOL price

- `/track btc 1` — subscribe to price updates (in minutes)
- `/untrack btc` — stop tracking coin
- `/list` — show active subscriptions

- `/help` — show main user commands
- `/hide` — remove old keyboard

## Project Structure
- `bot.py` — Telegram bot logic
- `price_checker.py` — price API and state logic
- `state.json` — saved coin prices
- `subscriptions.json` — user subscriptions (ignored by Git)
- `notes.md` — lesson notes
- `code_skeletons/` — practice skeleton files
- `requirements.txt` — project dependencies
- `.env` — bot token (not uploaded)
- `.gitignore` — ignored files

## Installation
`pip install -r requirements.txt`

## Run
`python bot.py`

## Environment
Create a `.env` file and add:

`BOT_TOKEN=your_telegram_bot_token`

## Notes
- The bot uses CoinGecko API
- Supported coins right now: `btc`, `eth`, `sol`
- Users can subscribe to price updates with custom intervals
- Subscriptions are stored in `subscriptions.json`
- Saved prices are stored in `state.json`
- The bot checks subscriptions every 30 seconds
- Uses `python-telegram-bot[job-queue]`