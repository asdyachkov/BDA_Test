from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.StartKeyboards import start_keyboard


async def bot_start(message: types.Message, state: FSMContext):
    """
    Обработчик на стартовое сообшение (/start)
    :param message: Сообщение от пользователя
    :param state: Текущее состояние
    :return:
    """
    text = [
        "Привет!",
        "Я умею определять текущую погоду 🌡️",
        "Конвертировать валюты 💵",
        "Отправлять случайную картинку с котиками 🐈",
        "Создавать опросы 📊",
        "",
        "Чтобы воспользоваться любой из функций, нажми на кнопку ниже",
        "В любой момент можно прервать выполнение любой из операций, введя /start",
    ]

    await message.answer("\n".join(text), reply_markup=start_keyboard)
    await state.finish()


def register_start(dp: Dispatcher):
    """
    Привязка обработчиков и хендлеров
    :param dp: Диспатчер
    :return: None
    """
    dp.register_message_handler(
        bot_start, state=["*"], commands=["start"], commands_prefix="!/"
    )
