from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot_template.tgbot.keyboards.StartKeyboards import start_keyboard


async def bot_start(message: types.Message, state: FSMContext):
    text = [
        "Привет!",
        "Я умею определять текущую погоду,",
        "Конвертировать валюты,",
        "Отправлять случайную картинку с котиками,",
        "Создавать опросы.",
        "",
        "Чтобы воспользоваться любой из функций, нажми на кнопку ниже",
    ]

    await message.answer("\n".join(text), reply_markup=start_keyboard)
    await state.finish()


def register_start(dp: Dispatcher):
    dp.register_message_handler(
        bot_start, state=["*"], commands=["start"], commands_prefix="!/"
    )
