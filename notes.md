## Crypto Price Bot — версия 1

### commands
/price btc -> показать цену BTC
/price eth -> показать цену ETH
/price sol -> показать цену SOL

/check -> проверить изменение цены BTC
/show -> показать сохранённую цену BTC
/reset -> сбросить сохранённую цену BTC

---

### API request
`get_coin_price(symbol)` -> получить цену монеты с API CoinGecko

`requests.get(url, params=params, timeout=10)` -> отправить GET-запрос

`response.json()` -> превратить JSON в словарь

`data[coin_id]["usd"]` -> достать цену

---

### coin mapping
`coin_map` -> переводит:
- btc -> bitcoin
- eth -> ethereum
- sol -> solana

`coin_map.get(symbol.lower())` -> получить нужную монету

---

### error handling
`try/except` -> защита от ошибок запроса

`status_code != 200` -> проверка ответа сервера

`return None` -> если цена не получена

---

### None
`None` -> означает "нет результата" или "не удалось получить данные"

используется:
- если API не ответил
- если монета не найдена

---

### state
`state.txt` -> хранит последнюю сохранённую цену (BTC)

`read_last_price()` -> прочитать цену

`write_last_price(price)` -> записать цену

---

### compare
`check_price_change(symbol)` -> сравнить текущую и прошлую цену

`current_price != last_price` -> проверка изменения

`difference = current_price - last_price` -> разница

`abs(difference)` -> убрать минус

`:.2f` -> формат числа

---

### first run
если файл пустой:
`write_last_price(current_price)`

---

### bot logic
`context.args` -> аргументы команды

`symbol = context.args[0]` -> получить монету

`symbol.upper()` -> красиво вывести BTC / ETH / SOL

---

### current limitations
- `/check`, `/show`, `/reset` работают только с BTC
- используется один `state.txt`

