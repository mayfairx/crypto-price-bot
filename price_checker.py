import requests
import time

last_cached_price = None
last_cached_time = 0
cache_seconds = 10

def get_btc_price():
    global last_cached_price, last_cached_time

    now = time.time()

    if last_cached_price is not None and now - last_cached_time < cache_seconds:
        return last_cached_price

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code !=200:
            return None
        
        data = response.json()

        if "bitcoin" not in data:
            return None
        
        price = data["bitcoin"]["usd"]
        last_cached_price = price
        last_cached_time = now

        return price
    
    except requests.RequestException:
        return None

def read_last_price():
    try:
        with open("state.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""
    
def write_last_price(price):
    with open("state.txt", "w", encoding="utf-8") as file:
        file.write(str(price))

def check_price_changed():
    current_price = get_btc_price()

    if current_price is None:
        return "Could not get BTC price from API."

    last_price = read_last_price()

    if last_price:
        last_price = float(last_price)

        if current_price != last_price:
            difference = current_price - last_price
            write_last_price(current_price)

            if difference > 0:
                return (
                    f"Price changed.\n\n"
                    f"Old price: ${last_price}\n"
                    f"New price: ${current_price}\n"
                    f"Difference: +${difference:.2f}"
                )
            else:
                return (
                    f"Price changed.\n\n"
                    f"Old price: ${last_price}\n"
                    f"New price: ${current_price}\n"
                    f"Difference: -${abs(difference):.2f}"
                )
        else:
            return f"No changes.\n\nCurrent price: ${current_price}"
    else:
        write_last_price(current_price)
        return f"First saved price: ${current_price}"

def reset_price():
    with open("state.txt", "w", encoding="utf-8") as file:
        file.write("")

def show_saved_price():
    saved_price = read_last_price()

    if saved_price:
        return f"Saved price: ${saved_price}"
    else:
        return "No saved price."