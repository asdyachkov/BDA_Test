from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callbacks.ConverterKeyboardsCallback import (
    ConverterKeyboardsCallback,
)


choose_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="RUB", callback_data=ConverterKeyboardsCallback.new(choiсe="RUB")
            ),
            InlineKeyboardButton(
                text="USD", callback_data=ConverterKeyboardsCallback.new(choiсe="USD")
            ),
        ],
        [
            InlineKeyboardButton(
                text="EUR", callback_data=ConverterKeyboardsCallback.new(choiсe="EUR")
            ),
            InlineKeyboardButton(
                text="CNY", callback_data=ConverterKeyboardsCallback.new(choiсe="CNY")
            ),
        ],
        [
            InlineKeyboardButton(
                text="Выход",
                callback_data=ConverterKeyboardsCallback.new(choiсe="back"),
            )
        ],
    ]
)
