# Проект "Short Link Service"

Это простой веб-сервис, предоставляющий функционал по созданию коротких ссылок, переходу по ним и удалению. Для работы с базой данных используется MongoDB. 

## Инструкция по запуску

1. Установите [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/), если они еще не установлены.

2. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/your_username/short-link-service.git
   cd short-link-service
   ```

3. Поменяйте файл `.env` в корне проекта и укажите необходимые переменные окружения, но это необязательно. Пример:

   ```dotenv
   MONGODB_URI=mongodb://mongo:27017/
   MONGODB_DB=short_link_bd
   ```

4. Запустите базу данных с помощью Docker Compose:

   ```bash
   docker-compose up --build
   ```

   Эта команда поднимет MongoDB.

5. Запустите приложение:

   ```bash
   uvicorn main:app --reload 
   ```

6. Приложение будет доступно по адресу [http://localhost:8000](http://localhost:8000).

## Функционал

### Создание короткой ссылки

Отправьте POST-запрос на `/short_link/` с JSON-телом, содержащим ключ `link` и значение URL, которое выхотите сохранить:

```bash
{
    "link": "https://example.com"
}
```

### Переход по короткой ссылке

Откройте браузер и перейдите по короткой ссылке:

```bash
http://localhost:8000/go/{short_link}
```

### Удаление короткой ссылки

Отправьте DELETE-запрос на `/del/` с JSON-телом, содержащим ключ `short_link`:

```bash
{
    "short_link": "http://127.0.0.1:8000/go/Gb659A"
}
```

## Зависимости

- [FastAPI](https://fastapi.tiangolo.com/): Веб-фреймворк для создания API на основе Python.
- [MongoDB](https://www.mongodb.com/): NoSQL база данных для хранения коротких ссылок.
- [Docker](https://www.docker.com/): Контейнеризация приложения и базы данных.

