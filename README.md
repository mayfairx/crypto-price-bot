# Crypto Price Bot

A simple Telegram bot built with Python that gets crypto prices from the CoinGecko API.

## Features
- `/price btc` — show BTC price
- `/price eth` — show ETH price
- `/price sol` — show SOL price
- `/check` — check BTC price change
- `/show` — show saved BTC price
- `/reset` — reset saved BTC price

## Project Structure
- `bot.py` — Telegram bot logic
- `price_checker.py` — price API and state logic
- `state.txt` — saved BTC price
- `notes.md` — lesson notes
- `code_skeletons/` — practice skeleton files
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
Right now:
- `/price` works for `btc`, `eth`, and `sol`
- `/check`, `/show`, and `/reset` work for BTC only