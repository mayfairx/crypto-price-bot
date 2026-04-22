import requests
import time

last_cached_price = ...
last_cached_time = ...
cache_seconds = ...

def get_btc_price():
    global ..., ...

    now = ...

    if ... is not None and ... - ... < ...:
        return ...

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "...",
        "vs_currencies": "..."
    }

    try:
        response = requests.get(..., ..., timeout=...)

        if response.status_code != ...:
            return ...

        data = response.json()

        if "..." not in data:
            return ...

        price = data["..."]["..."]
        last_cached_price = ...
        last_cached_time = ...

        return ...

    except requests.RequestException:
        return ...


def read_last_price():
    try:
        with open("...", "r", encoding="utf-8") as file:
            return file.read()....
    except FileNotFoundError:
        return "..."


def write_last_price(price):
    with open("...", "w", encoding="utf-8") as file:
        file.write(...(...))


def check_price_changed():
    current_price = ...()

    if current_price is None:
        return "..."

    last_price = ...()

    if last_price:
        last_price = ...(last_price)

        if current_price != last_price:
            difference = ... - ...
            ...(current_price)

            if difference > 0:
                return (
                    f"...\n\n"
                    f"... ${last_price}\n"
                    f"... ${current_price}\n"
                    f"... +${difference:.2f}"
                )
            else:
                return (
                    f"...\n\n"
                    f"... ${last_price}\n"
                    f"... ${current_price}\n"
                    f"... -${abs(difference):.2f}"
                )
        else:
            return f"...\n\n... ${current_price}"
    else:
        ...(current_price)
        return f"... ${current_price}"


def reset_price():
    with open("...", "w", encoding="utf-8") as file:
        file.write("...")


def show_saved_price():
    saved_price = ...()

    if saved_price:
        return f"... ${saved_price}"
    else:
        return "..."