import requests

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "...",
        "vs_currencies": "..."
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != ...:
            return None

        data = response.json()

        if "..." not in data:
            return None

        price = data["..."]["..."]
        return price

    except requests.RequestException:
        return None

def read_last_price():
    try:
        with open("state.txt", "r", encoding="utf-8") as file:
            return ...
    except FileNotFoundError:
        return "..."

def write_last_price(price):
    with open("state.txt", "w", encoding="utf-8") as file:
        file.write(...)

def check_price_change():
    current_price = get_btc_price()

    if current_price is None:
        return "..."

    last_price = read_last_price()

    if last_price:
        last_price = float(last_price)

        if current_price != last_price:
            difference = current_price - last_price
            write_last_price(current_price)

            if difference > 0:
                return (
                    f"Price changed.\n\n"
                    f"Old price: ${...}\n"
                    f"New price: ${...}\n"
                    f"Difference: +${...:.2f}"
                )
            else:
                return (
                    f"Price changed.\n\n"
                    f"Old price: ${...}\n"
                    f"New price: ${...}\n"
                    f"Difference: -${...:.2f}"
                )
        else:
            return f"No changes.\n\nCurrent price: ${...}"
    else:
        write_last_price(current_price)
        return f"First saved price: ${...}"

def reset_price():
    with open("state.txt", "w", encoding="utf-8") as file:
        file.write("")

def show_saved_price():
    saved_price = read_last_price()

    if saved_price:
        return f"Saved price: ${...}"
    else:
        return "..."