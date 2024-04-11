
Установите vault
```bash
sudo snap install vault
```

Запустите сервер Vault с помощью команды 
```
vault server -dev.  
```
После этой команды вы найдете свой токен:  

> Root Token: <YOUR_TOKEN>

В терминале запустите следующие команды:

```shell
export VAULT_ADDR='http://127.0.0.1:8200'
```
```shell
export VAULT_TOKEN='<YOUR_TOKEN>'
```

Напишите в файле **vault_utils.py**, ваш токен.
```python
client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='<ROOT_TOKEN>',
)
```
Запишите в поля ваши ключи и запустите скрипт.
```python
    create_secret('SERP_API_KEY', '<TOKEN>')
    create_secret('GOOGLE_API_KEY', '<TOKEN>')
    create_secret('GOOGLE_SEARCH_ENGINE_ID', '<TOKEN>')
    create_secret('TELEGRAM_TOKEN', '<TOKEN>')
    create_secret('VK_TOKEN', '<TOKEN>')
```
