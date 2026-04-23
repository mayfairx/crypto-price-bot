## Crypto Price Bot — версия 2 (multi-coin)

### commands
/price btc -> показать цену BTC  
/price eth -> показать цену ETH  
/price sol -> показать цену SOL  

/check btc -> проверить изменение цены BTC  
/check eth -> проверить изменение цены ETH  
/check sol -> проверить изменение цены SOL  

/show btc -> показать сохранённую цену BTC  
/show eth -> показать сохранённую цену ETH  
/show sol -> показать сохранённую цену SOL  

/reset btc -> сбросить сохранённую цену BTC  
/reset eth -> сбросить сохранённую цену ETH  
/reset sol -> сбросить сохранённую цену SOL  

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

### state (multi-coin)
`get_state_filename(symbol)` -> создать файл для монеты  

пример:
- state_btc.txt  
- state_eth.txt  
- state_sol.txt  

---

### file logic
`read_last_price(symbol)` -> прочитать цену конкретной монеты  

`write_last_price(symbol, price)` -> записать цену конкретной монеты  

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
`write_last_price(symbol, current_price)`  

---

### bot logic
`context.args` -> аргументы команды  

пример:
/check btc -> ["btc"]  

`symbol = context.args[0]` -> получить монету  

`symbol.lower()` -> нормализовать ввод  

`symbol.upper()` -> красиво вывести BTC / ETH / SOL  

---

### current features
- несколько монет (btc, eth, sol)  
- отдельный state для каждой монеты  
- команды работают независимо  

---

### current limitations
- нет авто-уведомлений  
- нет подписки на цену  
- проверка только вручную  

---

### auto tracking
`/track_on` -> включить авто-проверку цен  

`/track_off` -> выключить авто-проверку  

---

### job queue
`job_queue.run_repeating(func, interval, first)` -> запуск функции по таймеру  

- `func` -> функция, которую запускать  
- `interval` -> как часто (в секундах)  
- `first` -> через сколько запустить первый раз  

---

### global
`global price_job` -> позволяет менять переменную вне функции  

используется, чтобы:
- сохранить запущенный таймер  
- потом остановить его  

---

### auto check logic
`send_price_update()` -> проверяет цену и отправляет сообщение  

если `"No changes."`:
- ничего не отправлять  

---

### state
`price_job = None` -> авто-трекинг выключен  

`price_job != None` -> авто-трекинг включен  

---

### stop job
`price_job.schedule_removal()` -> остановить таймер  

### JSON state
`state.json` -> один файл для хранения сохранённых цен

пример:
{
  "btc": 78322,
  "eth": 2336.38
}

`import json` -> подключить модуль для работы с JSON

`STATE_FILE = "state.json"` -> имя файла с состоянием

`read_state()` -> прочитать весь JSON-файл

`write_state(state)` -> записать весь словарь обратно в JSON

`json.load(file)` -> прочитать JSON из файла

`json.dump(state, file)` -> записать данные в JSON

---

### JSON price logic
`read_last_price(symbol)` -> достать цену монеты из `state.json`

`state.get(symbol.lower(), "")` -> получить цену или пустую строку

`write_last_price(symbol, price)` -> обновить цену монеты в JSON

`state[symbol.lower()] = price` -> записать цену конкретной монеты

`reset_price(symbol)` -> удалить монету из JSON

`del state[symbol.lower()]` -> удалить сохранённую цену монеты

### subscriptions
`subscriptions.json` -> хранит подписки пользователей

пример:
{
  "chat_id": {
    "btc": {
      "interval": 5,
      "last_check": 0
    }
  }
}

`/track btc 5` -> подписка на монету

`/untrack btc` -> отписка

---

### time logic
`time.time()` -> текущее время в секундах

`current_time - last_check` -> сколько прошло времени

если меньше интервала -> пропускаем

---

### job queue
`run_repeating(func, interval=30)` -> запуск функции каждые 30 секунд

используется для проверки подписок