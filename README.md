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

- `/help` — show main user commands
- `/hide` — remove old keyboard

## Project Structure
- `bot.py` — Telegram bot logic
- `price_checker.py` — price API and state logic
- `state_btc.txt` — saved BTC price
- `state_eth.txt` — saved ETH price
- `state_sol.txt` — saved SOL price
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
- Each coin has its own saved state file
- Supported coins right now: `btc`, `eth`, `sol`