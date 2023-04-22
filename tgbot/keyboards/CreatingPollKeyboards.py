from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callbacks.CreatingPollCallback import (
    CreatingPollCallback,
)

# Файл с клавиатурами для голосования

is_poll_anonymous = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да, анонимный ✅",
                callback_data=CreatingPollCallback.new(choiсe="True"),
            ),
            InlineKeyboardButton(
                text="Нет, не анонимный ❌",
                callback_data=CreatingPollCallback.new(choiсe="False"),
            ),
        ],
    ]
)

poll_type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Quiz", callback_data=CreatingPollCallback.new(choiсe="quiz")
            ),
            InlineKeyboardButton(
                text="Regular", callback_data=CreatingPollCallback.new(choiсe="regular")
            ),
        ],
    ]
)

is_allows_multiple_answers = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да ✅", callback_data=CreatingPollCallback.new(choiсe="yes")
            ),
            InlineKeyboardButton(
                text="Нет ❌", callback_data=CreatingPollCallback.new(choiсe="no")
            ),
        ],
    ]
)


def correct_type(answers: list):
    """
    Создание динамической клавиатуры (исходя из имходных данных)
    :param answers: ответы на голосование
    :return: InlineKeyboardMarkup
    """
    data = []
    for i, answer in enumerate(answers):
        data.append(
            [
                InlineKeyboardButton(
                    text=f"{answer}",
                    callback_data=CreatingPollCallback.new(choiсe=f"{i}"),
                ),
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=data)
