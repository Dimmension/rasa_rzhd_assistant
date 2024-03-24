## MinIO
MinIO - это решение для хранения обьектов. Он предоставляет API для взаимодействия с файлами на сервере.
### Запуск
Инструкция - https://min.io/docs/minio/container/index.html
1. Запуск докер контейнера
    ```sh
    mkdir -p ~/minio/data

    docker run \
    -p 9000:9000 \
    -p 9001:9001 \
    --name minio \
    -v ~/minio/data:/data \
    -e "MINIO_ROOT_USER=minioadmin" \
    -e "MINIO_ROOT_PASSWORD=minioadmin" \
    quay.io/minio/minio server /data --console-address ":9001"
    ```
2. Создание bucket'a
    Зайдите на 127.0.0.1:9000 -> Object Browser -> Create a Bucket -> Create Bucket

3. Создание ключей доступа
    Зайдите на 127.0.0.1:9000 -> Access Keys -> Create Access Key -> Create

4. Переменные среды

    __.env__
    ```
    ACCESS_KEY=<YOUR_ACCESS_KEY>
    SECRET_KEY=<YOUR_SECRET_KEY>
    ```

5. Взаимодействие
    1. Создание и активация виртуального окружения venv.

        >_Перейдите в директорию minio_storage перед созданием venv._
        
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
    2. Установка зависимостей
        ```bash
        pip install -r minio_requirements.txt
        ```
    В файле __utils_minio.py__ есть функции для загрузки и выгрузки файлов на MinIO.

    Можно использовать для взаимодействия ui интерфейс, через браузер 127.0.0.1:9000
