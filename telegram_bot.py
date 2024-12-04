# import re
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
#
# # Настройки SMTP Яндекса
# SMTP_SERVER = "smtp.yandex.ru"
# SMTP_PORT = 587
# SMTP_LOGIN = "your_email@yandex.ru"  # Ваш email на Яндексе
# SMTP_PASSWORD = "your_password"  # Ваш пароль от Яндекса
#
#
# # Функция для проверки корректности email
# def is_valid_email(email: str) -> bool:
#     # Регулярное выражение для проверки email
#     pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA0-9-.]+$"
#     return bool(re.match(pattern, email))
#
#
# # Функция, которая будет вызываться при старте бота
# def start(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text("Привет! Пожалуйста, введите свой email:")
#
#
# # Функция для обработки email
# def handle_email(update: Update, context: CallbackContext) -> None:
#     email = update.message.text
#     if is_valid_email(email):
#         context.user_data['email'] = email  # Сохраняем email пользователя
#         update.message.reply_text("Email принят. Теперь, пожалуйста, введите сообщение:")
#         return
#     else:
#         update.message.reply_text("Неверный формат email. Попробуйте снова.")
#
#
# # Функция для обработки текста сообщения
# def handle_message(update: Update, context: CallbackContext) -> None:
#     if 'email' not in context.user_data:
#         update.message.reply_text("Сначала введите свой email.")
#         return
#
#     message_text = update.message.text
#     recipient_email = context.user_data['email']
#
#     # Отправка email через SMTP
#     try:
#         send_email(recipient_email, message_text)
#         update.message.reply_text(f"Сообщение успешно отправлено на {recipient_email}.")
#     except Exception as e:
#         update.message.reply_text(f"Произошла ошибка при отправке email: {e}")
#
#
# # Функция для отправки email через SMTP
# def send_email(recipient_email: str, message_text: str) -> None:
#     # Подготавливаем сообщение
#     msg = MIMEMultipart()
#     msg['From'] = SMTP_LOGIN
#     msg['To'] = recipient_email
#     msg['Subject'] = "Сообщение от Telegram-бота"
#
#     # Текст сообщения
#     msg.attach(MIMEText(message_text, 'plain'))
#
#     # Устанавливаем соединение с SMTP сервером и отправляем письмо
#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()  # Обеспечиваем безопасное соединение
#         server.login(SMTP_LOGIN, SMTP_PASSWORD)  # Входим в аккаунт
#         server.sendmail(SMTP_LOGIN, recipient_email, msg.as_string())  # Отправляем письмо
#
#
# # Основная функция для запуска бота
# def main() -> None:
#     # Создание приложения с использованием токена API
#     application = Application.builder().token("TELEGRAM_API_KEY").build()
#
#     # Добавление обработчиков команд
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(MessageHandler(filters.TEXT, handle_email))  # Обработчик для email
#     application.add_handler(MessageHandler(filters.TEXT, handle_message))  # Обработчик для сообщения
#
#     # Запуск бота
#     application.run_polling()
#
#
# if __name__ == '__main__':
#     main()

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
from dotenv import load_dotenv
import os

# Загружаем переменные из файла .env
load_dotenv()

# Настройки SMTP Яндекса
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587
SMTP_LOGIN = os.getenv("SMTP_LOGIN")  # Получаем из .env
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Получаем из .env

# API-ключ Telegram
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")  # Получаем из .env

# Определение состояний для ConversationHandler
EMAIL, MESSAGE = range(2)

# Функция для проверки корректности email
def is_valid_email(email: str) -> bool:
    # Регулярное выражение для проверки email
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

# Функция, которая будет вызываться при старте бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Привет! Пожалуйста, введите свой email:")
    return EMAIL

# Функция для обработки email
async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    if is_valid_email(email):
        context.user_data['email'] = email  # Сохраняем email пользователя
        await update.message.reply_text("Email принят. Теперь, пожалуйста, введите сообщение:")
        return MESSAGE
    else:
        await update.message.reply_text("Неверный формат email. Попробуйте снова.")
        return EMAIL

# Функция для обработки текста сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if 'email' not in context.user_data:
        await update.message.reply_text("Сначала введите свой email.")
        return ConversationHandler.END

    message_text = update.message.text
    recipient_email = context.user_data['email']

    # Отправка email через SMTP
    try:
        send_email(recipient_email, message_text)
        await update.message.reply_text(f"Сообщение успешно отправлено на {recipient_email}.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при отправке email: {e}")

    return ConversationHandler.END

# Функция для отмены операции
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Операция отменена.")
    return ConversationHandler.END

# Функция для отправки email через SMTP
def send_email(recipient_email: str, message_text: str) -> None:
    # Подготавливаем сообщение
    msg = MIMEMultipart()
    msg['From'] = SMTP_LOGIN
    msg['To'] = recipient_email
    msg['Subject'] = "Сообщение от Telegram-бота"

    # Текст сообщения
    msg.attach(MIMEText(message_text, 'plain'))

    # Устанавливаем соединение с SMTP сервером и отправляем письмо
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Обеспечиваем безопасное соединение
        server.login(SMTP_LOGIN, SMTP_PASSWORD)  # Входим в аккаунт
        server.sendmail(SMTP_LOGIN, recipient_email, msg.as_string())  # Отправляем письмо

# Основная функция для запуска бота
def main() -> None:
    # Создание приложения с использованием токена API
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    # Создание ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Добавление обработчиков
    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
