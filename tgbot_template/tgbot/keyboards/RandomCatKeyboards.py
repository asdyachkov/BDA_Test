from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot_template.tgbot.keyboards.callbacks.RandomCatKeyboardsCallback import (
    RandomCatKeyboardsCallback,
)


cat_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Еще котика!",
                callback_data=RandomCatKeyboardsCallback.new(choiсe="cat"),
            ),
        ],
    ]
)
