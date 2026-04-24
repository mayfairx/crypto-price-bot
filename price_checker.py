import requests
import json

STATE_FILE = "state.json"

def read_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file)

def get_coin_price(symbol):

    coin_map = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana"
    }

    coin_id = coin_map.get(symbol.lower())

    if not coin_id:
        return None

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None
        
        data = response.json()

        if coin_id not in data:
            return None
        
        price = data[coin_id]["usd"]

        return price
    
    except requests.RequestException:
        return None

def read_last_price(symbol):
    state = read_state()
    return state.get(symbol.lower(), "")
    
def write_last_price(symbol, price):
    state = read_state()
    state[symbol.lower()] = price
    write_state(state)

def check_price_change(symbol):
    current_price = get_coin_price(symbol)

    if current_price is None:
        return "Could not get coin price from API."

    last_price = read_last_price(symbol)

    if last_price:
        last_price = float(last_price)

        if current_price != last_price:
            difference = current_price - last_price
            write_last_price(symbol, current_price)

            if difference > 0:
                return (
                    f"{symbol.upper()}\n\n"
                    f"${current_price:,.2f} 📈 +${difference:,.2f}"
                )
            else:
                return (
                    f"{symbol.upper()}\n\n"
                    f"${current_price:,.2f} 📉 -${abs(difference):,.2f}"
                )
        else:
            return (
                f"{symbol.upper()}\n\n"
                f"${current_price:,.2f}\n"
                f"no changes"
            )
    else:
        write_last_price(symbol, current_price)
        return (
            f"{symbol.upper()}\n\n"
            f"${current_price:,.2f}\n"
            f"tracking started"
        )  

def reset_price(symbol):
    state = read_state()

    if symbol.lower() in state:
        del state[symbol.lower()]
        write_state(state)
        return f"{symbol.upper()}\n\nsaved price reset"
    else:
        return f"{symbol.upper()}\n\nno saved price"

def show_saved_price(symbol):
    saved_price = read_last_price(symbol)

    if saved_price:
        return (
            f"{symbol.upper()}\n\n"
            f"${float(saved_price):,.2f}\n"
            f"saved price"
        )
    else:
        return f"{symbol.upper()}\n\nno saved price"
