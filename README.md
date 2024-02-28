# Документация "Ассистент РЖД"
__Ассистент РЖД__ - это чатбот, который поможет ответить на интересующие вопросы по теме ПТЭ. Чатбот написан с использованием платформы с открытым исходным кодом RASA.

## Поисковая система

Ассистент поддерживает поиск в интернете. Чтобы попросить бота найти что-то в интернете, необходимо ввести одну из ключевых команд: __"найди"__ или __"поищи"__.

После этого вам будет предложено ввести запрос, бот найдет для вас релевантную информацию по запросу и выдаст вам __текстовый ответ__ или __ссылки на ресурсы__, которые могут вам помочь. 

Поиск происходит с использованием __[Google Custom Search API](https://developers.google.com/custom-search/v1/overview?hl=ru)__ или __[SerpApi](https://serpapi.com/)__. 
### Как происходит поиск?
Сначала запрос принимает SerpApi и возвращает JSON страницы результатов поиска (SERP) Google, после этого если на SERP странице был раздел "Вопросы по теме" (в анг. "People also ask"), то бот выдает ответ на первый вопрос в этом разделе(механизмы google достаточно хорошо справляются и выдают очень релевантные результаты). 

В случае если первая часть поискового механизма не справилась или закончились запросы у SerpApi, поиск происходит с использованием Google Custom Search API, он также возвращает JSON страницы результатов поиска Google. Но в данном случае пользователь получает релевантные ссылки ([Wikipedia](https://en.wikipedia.org/wiki/Main_Page) ставится в первый приоритет). 
## Поддерживаемые платформы
Взаимодействие (общение, диалог, запросы) с ассистентом может происходить на следующих платформах:
- [Telegram](https://web.telegram.org/)
- [Discord](https://discord.com/)
- [VK](https://vk.com/)

> Для коннекта между мессенжерами и моделью RASA, были использованы Rasa Custom Connectors. 

## Режимы работы
В ходе работы было реализовано два варианта работы с мессенжерами.
1. __Моноканальность__
В этом режиме запросы  отправлялись в один узел входа/выхода на сервере Rasa, и не обрабатывалось с какого канала пришёл запрос, не было асинхронности. Проще говоря начать общение можно было в Телеграме, а закончить в ВК. 

2. __Мультиканальность__
В данном режиме используется несколько узлов входа/выхода, запроосы с разных ресурсов обрабатываются отдельно друг от друга, сервер Rasa знает кто прислал запрос. В данном варианте реалаизации работы, можно настроить так, чтобы ввод был только в одном канале, а вывод в другом, или все в одном канале.

## Установка
1. Склонируйте репозиторий
	```bash
	git clone https://github.com/Dimmension/rasa_work.git
	```
2. Создание виртуального окружения venv
	```bash
	python3 -m venv venv
	source ./venv/bin/activate
	```
3. Установка зависимостей
	```bash
	pip install -r rasa_requirements.txt
	```
## Настройка

1. __Настройка ngrok__
	
	[__Гайд ngrok__](https://ngrok.com/docs/getting-started/)
	```bash
	ngrok config add-authtoken <TOKEN>
	```
	Здесь необходимо создать свой аккаунт __ngrok__ и получить токен, а также создать __свой__ статический домен
	```bash
	ngrok http --domain=<YOUR URL> 5005
	```

2. __Токены__ 
Вам потребуется получить токены в той среде взаимодействия в которой вы хотите, чтобы он использовался, а потом вписать их в __credentials.yml__:

	__Telegram__
	_Инструкция получения данных для телеграма: https://core.telegram.org/bots/tutorial#getting-ready_
	```yml
	### credentials.yml
	access_token: 'YOUR_TOKEN'
	verify: 'BOT_USERNAME'
	webhook_url: 'https://<YOUR URL FROM NGROK>/webhooks/telegram/webhook'
	```

	__VK__
	_Инструкция получения данных для ВК: https://dev.vk.com/ru/api/callback/getting-started_
	```yml
	### credentials.yml
	access_token: 'YOUR_TOKEN'
	secret_key: 'SECRET_KEY'
	webhook_url: 'https://<YOUR URL FROM NGROK>/webhooks/vk/webhook'
	```

## Запуск
#### Запуск в разных режимах работы
1. В режиме консоли:
	```bash
	rasa shell # Запуск модели rasa
	```
	```bash
	rasa run actions # Запуск custom actions
	```
2. С использованием мессенджеров(Мультиканальность)
		
	```bash
	rasa run --enable-api --cors "*" # Запуск модели 
	```
	```bash
	rasa run actions # Запуск custom actions
	```
3. С использованием мессенджеров(Моноканальность)
		
	```bash
	rasa run --enable-api --cors "*" # Запуск модели 
	```
	```bash
	rasa run actions # Запуск custom actions
	```


    Нужно создать еще один venv для запуска ботов, по причине того что есть конфликты библиотек
    ```bash
    python3 -m venv venv_bots
    source ./venv_bots/bin/activate
    ```
    ```bash
    pip install -r bots_requirements.txt
    ```
    ```bash
    python3 bots/telegram_api_bot.py
    python3 bots/vk_api_bot.py
    python3 bots/discord_api_bot.py
    ```

## Переменные окружения
В директориях __bots__ и __actions__ надо создать __.env__ файлы со следующим содержанием.

___.env (actions)___
```python
SERP_API_KEY = "<YOUR_TOKEN>"

GOOGLE_API_KEY = "<YOUR_TOKEN>>"
GOOGLE_SEARCH_ENGINE_ID = "<YOUR_TOKEN>"

URL_SERPAPI_STATS_PAGE = "https://serpapi.com/account?api_key="
URL_GOOGLE_SEARCH = "https://customsearch.googleapis.com/customsearch/v1"
```

___.env (bots)___
```python
TELEGRAM_TOKEN = "<YOUR_TOKEN>" 
VK_TOKEN = "<YOUR_TOKEN>"
DISCORD_TOKEN = "<YOUR_TOKEN>"
```
