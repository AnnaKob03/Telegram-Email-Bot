# Telegram Email Bot

Этот проект представляет собой Telegram-бота, который позволяет пользователю отправлять электронные письма с помощью почтового сервиса SMTP (например, Яндекс) через Telegram. Пользователь вводит свой email и сообщение, и бот отправляет это сообщение на указанный email.

## Требования

Перед запуском проекта убедитесь, что у вас установлен Python 3.7+ и все необходимые зависимости, которые указаны в файле `requirements.txt`.

### Установка зависимостей

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/telegram_email_bot.git
   cd telegram_email_bot
   ```
2. Создайте виртуальное окружение и активируйте его:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Установите зависимости из requirements.txt:

   ```bash
   pip install -r requirements.txt
   ```
### Файл .env

В корне проекта должен быть файл .env, который содержит важные конфиденциальные переменные для подключения к SMTP серверу и Telegram API.
Создайте файл .env и добавьте следующие строки:

   ```bash
   SMTP_LOGIN=your_email@yandex.ru
   SMTP_PASSWORD=your_password
   TELEGRAM_API_KEY=your_telegram_bot_api_key
   ```
- SMTP_LOGIN: Ваш email для SMTP (например, Яндекс)
- SMTP_PASSWORD: Ваш пароль от SMTP почтового сервиса.
- TELEGRAM_API_KEY: Ваш API-ключ для Telegram-бота. Получить его можно, зарегистрировав бота через BotFather.

### Запуск бота

1. Убедитесь, что файл .env существует и содержит правильные данные.

2. Запустите скрипт telegram_bot.py:

   ```bash
   python telegram_bot.py
   ```
Бот начнёт работать и будет готов принимать сообщения через Telegram. Чтобы начать, просто отправьте команду /start в чат с ботом.