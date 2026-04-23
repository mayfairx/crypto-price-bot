import requests

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

def get_state_filename(symbol):
    return f"state_{symbol.lower()}.txt"

def read_last_price(symbol):
    filename = get_state_filename(symbol)

    try: 
        with open(filename, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""
    
def write_last_price(symbol, price):
    filename = get_state_filename(symbol)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(price))

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
                    f"{symbol.upper()} price changed.\n\n"
                    f"Old price: ${last_price}\n"
                    f"New price: ${current_price}\n"
                    f"Difference: +${difference:.2f}"
                )
            else:
                return (
                    f"{symbol.upper()} price changed.\n\n"
                    f"Old price: ${last_price}\n"
                    f"New price: ${current_price}\n"
                    f"Difference: -${abs(difference):.2f}"
                )
        else:
            return f"No changes.\n\nCurrent {symbol.upper()} price: ${current_price}"
    else:
        write_last_price(symbol, current_price)
        return f"First saved {symbol.upper()} price: ${current_price}"

def reset_price(symbol):
    filename = get_state_filename(symbol)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("")

    return f"Saved {symbol.upper()} price reset."

def show_saved_price(symbol):
    saved_price = read_last_price(symbol)

    if saved_price:
        return f"Saved {symbol.upper()} price: ${saved_price}"
    else:
        return f"No saved {symbol.upper()} price."
