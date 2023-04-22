from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callbacks.RandomCatKeyboardsCallback import (
    RandomCatKeyboardsCallback,
)

# Файл с клавиатурами для котиков

cat_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Еще котика! 🐈",
                callback_data=RandomCatKeyboardsCallback.new(choiсe="cat"),
            ),
        ],
    ]
)
