import json

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from environs import Env

from services.open_weather_parser import get_weather
from misc.states import WeatherStates

from keyboards.callbacks.StartKeyboardsCallback import (
    StartKeyboardsCallback,
)


async def bot_weather_start(call: CallbackQuery, state: FSMContext):
    text = [
        "Введите город, в котором хотите узнать текущую погоду",
        "Принимаются только города, написанные английскими буквами!",
        "Например, Саратов запишите как Saratov",
    ]

    await call.message.edit_text("\n".join(text))
    await state.set_state(WeatherStates.S1)


async def bot_weather_answer(message: types.Message, state: FSMContext):
    env = Env()
    env.read_env(".env")
    weather_data = json.loads(
        await get_weather(message.text.lower(), env.str("OPEN_WEATHER_TOKEN"))
    )
    if "error" not in weather_data.keys():
        text = [
            f"Погода в городе: {weather_data['city']}",
            f"{weather_data['weather_description']}",
            f"Температура: {weather_data['current_temperature']}C°",
            f"Влажность: {weather_data['current_humidity']}%",
            f"Давление: {weather_data['current_pressure']} мм.рт.ст",
            f"Ветер: {weather_data['current_wind_speed']} м/с",
            f"Хорошего дня!",
        ]

        await message.answer("\n".join(text))
        await state.finish()
    else:
        text = [
            "Не могу найти введенный Вами город",
            "Поробуйте еще раз",
        ]

        await message.answer("\n".join(text))


def register_weather(dp: Dispatcher):
    dp.register_callback_query_handler(
        bot_weather_start, StartKeyboardsCallback.filter(choiсe="weather")
    )
    dp.register_message_handler(bot_weather_answer, state=WeatherStates.S1)
