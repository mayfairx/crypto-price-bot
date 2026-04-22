## Урок 1 — Crypto price bot: первая версия

### API request
`def get_btc_price():` -> получить цену BTC с API

`requests.get(url, params=params)` -> отправить GET-запрос к API

`response.json()` -> превратить ответ JSON в словарь Python

`data["bitcoin"]["usd"]` -> достать цену BTC в долларах

### error handling
`try/except` -> защита от ошибок запроса

`timeout=10` -> ждать ответ максимум 10 секунд

`response.status_code` -> проверить, успешно ли ответил сервер

`return None` -> вернуть пустое значение, если API не дал цену

### cache
`last_cached_price` -> хранить последнюю цену в памяти

`last_cached_time` -> хранить время последнего успешного запроса

`cache_seconds = 10` -> сколько секунд использовать кэш

`time.time()` -> получить текущее время

`if last_cached_price is not None and now - last_cached_time < cache_seconds:` -> вернуть цену из кэша, если она ещё свежая

### state
`state.txt` -> файл, который хранит последнюю сохранённую цену

`read_last_price()` -> прочитать прошлую цену из `state.txt`

`write_last_price(price)` -> записать новую цену в `state.txt`

`file.read().strip()` -> убрать лишние пробелы и переносы строки

### compare
`check_price_changed()` -> сравнить текущую цену с прошлой

`if current_price is None:` -> проверить, удалось ли получить цену

`if current_price != last_price:` -> проверить, изменилась ли цена

`difference = current_price - last_price` -> посчитать разницу

`if difference > 0:` -> цена выросла

`else:` -> цена упала

`abs(difference)` -> убрать минус у отрицательного числа

`:.2f` -> показать число с двумя знаками после точки

### show/reset
`reset_price()` -> очистить `state.txt`

`show_saved_price()` -> показать, что сейчас сохранено в `state.txt`

`return "No saved price."` -> сообщение, если файл пустой

### bot
`from price_checker import ...` -> импортировать функции логики в бота

`async def price(...)` -> команда `/price`

`async def check(...)` -> команда `/check`

`async def reset(...)` -> команда `/reset`

`async def show(...)` -> команда `/show`

`await update.message.reply_text(...)` -> отправить сообщение в Telegram

`app.add_handler(CommandHandler(...))` -> привязать команду к функции

`app.run_polling()` -> запустить бота