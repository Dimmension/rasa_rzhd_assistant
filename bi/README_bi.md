## BI Rasa
BI Rasa - решение для сбора информации о диалоговых сессиях Rasa и их анализа с помощью сервиса DataLens. 

### Запуск PostgresDB Docker
Решение будет использовать PostgresSQL базу данных в докер контейнере.

```sh
docker run -d \
    --name test \
    -e POSTGRES_USER=test \
    -e POSTGRES_PASSWORD=test \
    -p 38746:5432 \
    postgres:15.5
```

### Изменение в проекте Rasa
Необходимо добавить данные своей БД в tracker store в __credentials.yml__, место куда сохраняется логи о диалоговых сессиях
```yml
### credentials.yml
tracker_store:
    type: SQL
    dialect: "postgresql"  # the dialect used to interact with the db
    url: "localhost"  # (optional) host of the sql db, e.g. "localhost"
    db: "test"  # path to your db
    username: "test" # username used for authentication
    password: "test" # password used for authentication
```
Теперь все логи будут сохранятся в развернутой базе данных.

### Обработка информации о диалоговых сессиях
1. Создание и активация виртуального окружения venv.

	>_Перейдите в директорию bi перед созданием venv._
	
	__Linux__
	```bash
	python3 -m venv venv
	source ./venv/bin/activate
	```
	__Windows(cmd)__
	```bash
	python -m venv venv
	venv\Scripts\activate.bat
	```
	__Windows(PowerShell)__
	```bash
	python -m venv venv
	venv/Scripts/Activate.ps1
	```
2. Установка пакетов
	Минимальные пакеты для запуска rasa в режиме shell.
	```bash
	pip install -r bi_requirements.txt
	```
3. Переменные среды

    __.env__
    ```
    PG_HOST=localhost
    PG_PORT=5432
    PG_USER=test
    PG_PASSWORD=test
    PG_DBNAME=test
    ```

4. Обработка логов
    С помощью скрипта __db_convertor.py__, мы получим csv файлы с необходимыми данными.
    Даллее их необходимо будет загрузить на BI платформу DataLens
    ```sh
    python3 db_convertor.py 
    ```
    Появится два файла __intent_data.csv__ и __request_data.csv__

### DataLens
Пошаговая инструкция по загрузке и вузуалищации csv от Яндекса [__здесь__](https://cloud.yandex.ru/ru/docs/tutorials/datalens/data-from-csv-visualization)