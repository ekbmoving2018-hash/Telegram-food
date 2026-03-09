# Telegram-бот «Что приготовить»

Бот предлагает рецепты по списку продуктов с помощью OpenAI API.

## Стек

- Python 3.12
- aiogram 3
- FastAPI
- OpenAI Responses API
- uvicorn
- Docker

## Архитектура

```
Telegram -> webhook -> FastAPI -> aiogram -> OpenAI API -> ответ в Telegram
```

Используется webhook (без polling). Проект готов к деплою на [Railway](https://railway.com).

## Локальный запуск

1. Клонируйте репозиторий и перейдите в папку проекта.

2. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # или: .venv\Scripts\activate  # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Скопируйте и заполните переменные окружения:
   ```bash
   cp .env.example .env
   ```
   Отредактируйте `.env`:
   - `TELEGRAM_BOT_TOKEN` — токен от [@BotFather](https://t.me/BotFather)
   - `OPENAI_API_KEY` — ключ OpenAI
   - `WEBHOOK_BASE_URL` — публичный HTTPS-URL (для локального теста можно использовать [ngrok](https://ngrok.com))

5. Запустите приложение:
   ```bash
   uvicorn main:app --reload
   ```

## Деплой на Railway

1. Зарегистрируйтесь на [railway.com](https://railway.com) и создайте проект.

2. Подключите GitHub-репозиторий или загрузите код через Railway CLI.

3. Добавьте переменные окружения:
   | Переменная | Описание |
   |------------|----------|
   | `TELEGRAM_BOT_TOKEN` | Токен бота от @BotFather |
   | `OPENAI_API_KEY` | API-ключ OpenAI |
   | `OPENAI_MODEL` | Модель (по умолчанию: gpt-4.1) |
   | `WEBHOOK_BASE_URL` | URL приложения: `https://${{RAILWAY_PUBLIC_DOMAIN}}` |
   | `WEBHOOK_PATH` | Путь webhook (по умолчанию: /webhook) |

4. Railway задаёт `PORT` и `RAILWAY_PUBLIC_DOMAIN` автоматически.  
   Для `WEBHOOK_BASE_URL` можно использовать:  
   `https://<ваш-сервис>.railway.app`

5. Выберите способ деплоя: **Dockerfile** (в проекте уже есть Dockerfile).

6. После деплоя Railway выдаст публичный URL. Укажите его в `WEBHOOK_BASE_URL` и при необходимости перезапустите сервис.

7. Бот будет принимать обновления по адресу:  
   `https://<ваш-url>/webhook`

## Переменные окружения

| Переменная | Обязательная | По умолчанию |
|------------|-------------|--------------|
| `TELEGRAM_BOT_TOKEN` | Да | — |
| `OPENAI_API_KEY` | Да | — |
| `WEBHOOK_BASE_URL` | Да | — |
| `OPENAI_MODEL` | Нет | gpt-4.1 |
| `WEBHOOK_PATH` | Нет | /webhook |
| `PORT` | Нет | 8000 |

## Использование

1. Запустите бота командой `/start`.
2. Отправьте список продуктов в произвольной форме, например:  
   `яйца, сыр, помидоры, хлеб`
3. Бот ответит рецептом в формате:
   - Название блюда
   - Что понадобится
   - Как готовить (пошагово)
   - Время приготовления
   - Совет

## Требования к OpenAI

Используется OpenAI Responses API (клиент `openai>=1.55`). Если Responses API недоступен в вашей версии SDK, обновите библиотеку или временно переключитесь на Chat Completions в `bot/openai_client.py`.
