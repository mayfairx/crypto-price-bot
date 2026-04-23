import requests
import json

STATE_FILE = "..."

def get_coin_price(symbol):
    coin_map = {
        "btc": "...",
        "eth": "...",
        "sol": "..."
    }

    coin_id = coin_map.get(symbol.lower())

    if not coin_id:
        return None

    try:
        response = requests.get(..., params=..., timeout=10)

        if response.status_code != ...:
            return None

        data = response.json()

        if coin_id not in data:
            return None

        return data[coin_id]["usd"]

    except requests.RequestException:
        return None

def read_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file)

def read_last_price(symbol):
    state = read_state()
    return state.get(..., "")

def write_last_price(symbol, price):
    state = read_state()
    state[...] = price
    write_state(state)

def check_price_change(symbol):
    current_price = get_coin_price(symbol)

    if current_price is None:
        return "..."

    last_price = read_last_price(symbol)

    if last_price:
        last_price = float(last_price)

        if current_price != last_price:
            difference = current_price - last_price
            write_last_price(symbol, current_price)

            if difference > 0:
                return ...
            else:
                return ...
        else:
            return ...
    else:
        write_last_price(symbol, current_price)
        return ...

def reset_price(symbol):
    state = read_state()

    if symbol.lower() in state:
        del state[symbol.lower()]
        write_state(state)
        return ...
    else:
        return ...

def show_saved_price(symbol):
    saved_price = read_last_price(symbol)

    if saved_price:
        return ...
    else:
        return ...