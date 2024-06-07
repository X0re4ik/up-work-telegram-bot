# Для разработчиков

1. Установка виртуального окружения
```
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ make pip-requirements
```

2. Установить файл `.env` пример смотреть в `.example.env`
```
$ nano .env
...
TELEGRAM_TOKEN=7057675274:AAGE9cZU3-ZqFUrnjItFZvNwPhwZMLq17t0

REDIS_HOST=localhost
REDIS_PORT=6379

// Параметры сервиса авторизации
BACKEND_API_HOST=localhost 
BACKEND_API_PORT=8000
BACKEND_API_PROTOCOL=http
BACKEND_API_DEFAULT_PATH=api/v1
...
```

3. Запустить внешний сервис `redis`:
```
$ make dev-services
```

4. Запустить сервер бота
```
$ source entrypoints/bot.sh
```


# Deploy
1. Устанавливаем переменные окружения в `.docker-compose.prod.env`
```
$ nano .docker-compose.prod.env
TELEGRAM_TOKEN=7057675274:AAGE9cZU3-ZqFUrnjItFZvNwPhwZMLq17t0

REDIS_HOST=redis
REDIS_PORT=6379

BACKEND_API_HOST=147.45.137.19 # Ваш сервер
BACKEND_API_PORT=8000
BACKEND_API_PROTOCOL=http
BACKEND_API_DEFAULT_PATH=api/v1
```

2. Запускаем
```
$ make -f docker.Makefile restart
```
