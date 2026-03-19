# Chat Service

Приложение на FastAPI для управления пользователями и аутентификации (создание, получение, обновление, удаление пользователей, выдача/обновление токенов). Асинхронная работа с базой данных через SQLAlchemy + asyncpg.

## Содержание
- Требования
- Конфигурация
- Запуск в Docker
- Локальный запуск
- Запуск тестов
- Запуск тестов через Docker
- API — основные эндпоинты
- Примеры запросов (из OpenAPI)
- Структура проекта
- Контакты

## Требования
- Python 3.12+
- Docker и Docker Compose (или modern `docker compose`)
- Рекомендуется использовать виртуальное окружение

Зависимости перечислены в `requirements.txt`.

## Конфигурация

Проект читает переменные окружения из файлов в папке `conf` (например, `.env.dev`, `.env.test`, `.env.db`, `.env.testdb`).

Пример `conf/.env.dev` (для разработки / Docker):

```dotenv
DB_PREFIX=postgresql+asyncpg
DB_NAME=chat_db
DB_HOST=localhost      # при запуске через docker-compose — имя сервиса (app_db)
DB_USER=pyuser
DB_PASSWORD=float123
DB_PORT=5432
```

Пример `conf/.env.test` (для тестов, локально):

```dotenv
DB_PREFIX=postgresql+asyncpg
DB_NAME=test_chat_db
DB_HOST=localhost
DB_USER=pyuser
DB_PASSWORD=float123
DB_PORT=5432   # если у вас локальный Postgres слушает 5433, иначе 5432
```

Файлы для конфигурации контейнера БД (пример): `conf/.env.db`:

```dotenv
POSTGRES_USER=pydev
POSTGRES_PASSWORD=strongpassword123
POSTGRES_DB=chat_
OUTER_PORT=5434
```

`conf/.env.testdb` (для тестовой БД в `docker-compose`):

```dotenv
POSTGRES_USER=pydev
POSTGRES_PASSWORD=float123
POSTGRES_DB=test_chat_db
```

Убедитесь, что указанные базы созданы и доступны перед запуском (или используйте `docker compose`, который поднимает БД).

## Запуск в Docker

1. Создайте/обновите `conf/.env.dev` с нужными переменными окружения (см. выше).
2. Из корня проекта выполните один из вариантов:

```bash
# Используя modern docker CLI (рекомендуется)
docker compose up --build app

# Или, если у вас старая утилита docker-compose:
docker-compose up --build app
```

При запуске в Docker в `conf/.env.dev` должен быть `DB_HOST=app_db` (имя сервиса из `docker-compose.yml`).

Сервис `app` будет доступен на порту `8002` хоста (в `docker-compose.yml` указан маппинг `8002:8000`).

## Локальный запуск

1. Создайте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
# .\env\Scripts\activate  # Windows
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте/настройте `conf/.env.dev` (например, `DB_HOST=localhost` для локального Postgres) и запустите приложение:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Или используйте скрипты в `sh/` (например, `sh/run_app.sh`).

## Запуск тестов (локально)

1. Создайте `conf/.env.test` с настройками тестовой БД (см. выше).
2. Активируйте виртуальное окружение и выполните:

```bash
pytest -v test
```

Тесты находятся в директории `test` и включают unit и end-to-end тесты.

## Запуск тестов через Docker

В `docker-compose.yml` присутствуют сервисы `test_app` и `test_db`.

1. Убедитесь, что `conf/.env.test` и `conf/.env.testdb` заполнены (для контейнера тестовой БД).
2. Из корня проекта выполните (рекомендуется):

```bash
# Собрать образы и поднять тестовые контейнеры, выполнить тесты и вернуть код завершения
docker compose up --build --abort-on-container-exit --exit-code-from test_app test_db test_app
```

Или (альтернативно):

```bash
# Поднять тестовую БД и тестовый контейнер
docker compose up --build test_db test_app
```

Контейнер `test_app` запускает скрипт `sh/run_test.sh`, который выполняет тесты и сохраняет отчёты в папке `reports` (см. `docker/test.Dockerfile`). После завершения отчёты будут в `./reports` на хосте.

Совет по устранению проблем: если вы видите ошибку похожую на KeyError: 'ContainerConfig' при попытке пересоздать контейнеры, попробуйте удалить старые контейнеры/образы и volumes и запустить заново:

# Эндпоинты чатов

## Создать чат
**POST** `/chats/`

```bash
curl -s -X POST "http://localhost:8000/chats/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_ACCESS_TOKEN>" \
  -d '{
    "title": "Общий чат"
  }'
``` 

## Пример ответа (ChatResponse):
{
  "id": 1,
  "created_at": "2026-03-19T10:30:00.123Z",
  "title": "Общий чат"
}

## Отправить сообщение в чат
**POST** /chats/{chat_id}/messages

```bash
curl -s -X POST "http://localhost:8000/chats/1/messages" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_ACCESS_TOKEN>" \
  -d '{
    "text": "Привет, это тестовое сообщение!"
  }'
```
## Пример ответа (MessageResponseEntity):
```json
{
  "id": 1,
  "created_at": "2026-03-19T10:31:00.123Z",
  "text": "Привет, это тестовое сообщение!"
}
```
## Получить детали чата
**GET** /chats/{chat_id}/

```bash
curl -s -X GET "http://localhost:8000/chats/1/" \
  -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"
```
## Пример ответа (массив MessageResponseEntity):

```json
[
  {
    "id": 1,
    "created_at": "2026-03-19T10:31:00.123Z",
    "text": "Привет, это тестовое сообщение!"
  },
  {
    "id": 2,
    "created_at": "2026-03-19T10:32:00.123Z",
    "text": "Второе сообщение в чате"
  }
]
```

## Удалить чат
**DELETE** /chats/{chat_id}/

```bash
curl -s -X DELETE "http://localhost:8000/chats/1/" \
  -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"
```

При успешном удалении возвращается статус 204 No Content.
## Структура проекта (кратко)
- `app/` — исходники приложения (routers, services, repositories, schemas, middlewares)
- `db/` — подключение к БД, session manager
- `migrations/` — Alembic миграции
- `conf/` — конфигурационные файлы и env-шаблоны
- `docker/` — Dockerfile'ы
- `sh/` — утилиты запуска (run_app.sh, run_test.sh и т.д.)
- `test/` — тесты (unit и e2e)
- `reports/` — отчёты тестов (см. docker/test.Dockerfile)

## Контакты
- Репозиторий: https://github.com/danilaDDD/chat-api.gi
- Автор/контакт: Данила Никитин (danila.n2015@yandex.ru, +7 995 283 47-76)
