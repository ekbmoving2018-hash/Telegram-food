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

В проекте есть `railway.json` — конфигурация для Railway (Dockerfile, healthcheck, restart policy).

### Пошаговая настройка

1. **Создайте проект** на [railway.com](https://railway.com) (New Project → Deploy from GitHub repo).

2. **Подключите репозиторий** `ekbmoving2018-hash/Telegram-food`. Railway сам обнаружит Dockerfile.

3. **Добавьте публичный домен**: Service → Settings → Networking → Generate Domain.

4. **Задайте переменные окружения** (Service → Variables):

   | Переменная | Значение |
   |------------|----------|
   | `TELEGRAM_BOT_TOKEN` | Токен от @BotFather |
   | `OPENAI_API_KEY` | Ваш API-ключ OpenAI |
   | `WEBHOOK_BASE_URL` | `https://${{RAILWAY_PUBLIC_DOMAIN}}` |
   | `OPENAI_MODEL` | `gpt-4.1` (опционально) |

   Railway автоматически подставляет `RAILWAY_PUBLIC_DOMAIN` (например, `xxx.up.railway.app`).

5. **Деплой**: при пуше в main Railway автоматически пересоберёт и задеплоит приложение.

6. Webhook Telegram: `https://<ваш-домен>/webhook`

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
