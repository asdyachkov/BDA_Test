import json

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.callbacks.StartKeyboardsCallback import (
    StartKeyboardsCallback,
)
from tgbot.keyboards.callbacks.RandomCatKeyboardsCallback import (
    RandomCatKeyboardsCallback,
)
from tgbot.services.cat_photo_parser import cat_photo
from tgbot.keyboards.RandomCatKeyboards import cat_keyboard


async def cat_photo_send(call: CallbackQuery):
    cat_photo_data = json.loads(await cat_photo())

    if "error" not in cat_photo_data.keys():
        text = ["Вот и милый котик"]

        await call.message.answer_photo(
            cat_photo_data["cat_url"],
            caption="\n".join(text),
            reply_markup=cat_keyboard,
        )
    else:
        text = ["На стороне API возникла ошибка, котиков пока нет("]

        await call.message.answer("\n".join(text))


def register_cat_photo(dp: Dispatcher):
    dp.register_callback_query_handler(
        cat_photo_send, StartKeyboardsCallback.filter(choiсe="cat_photo")
    )
    dp.register_callback_query_handler(
        cat_photo_send, RandomCatKeyboardsCallback.filter(choiсe="cat")
    )
