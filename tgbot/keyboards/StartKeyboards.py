from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callbacks.StartKeyboardsCallback import (
    StartKeyboardsCallback,
)

# Файл с клавиатурами для стартового сообщения

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Определить текущую погоду 🌡️",
                callback_data=StartKeyboardsCallback.new(choiсe="weather"),
            )
        ],
        [
            InlineKeyboardButton(
                text="Конвертировать валюту 💵",
                callback_data=StartKeyboardsCallback.new(choiсe="converter"),
            )
        ],
        [
            InlineKeyboardButton(
                text="Картинка с котиком! 🐈",
                callback_data=StartKeyboardsCallback.new(choiсe="cat_photo"),
            )
        ],
        [
            InlineKeyboardButton(
                text="Создать опрос 📊",
                callback_data=StartKeyboardsCallback.new(choiсe="create_poll"),
            )
        ],
    ]
)
