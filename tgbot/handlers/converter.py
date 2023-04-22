import json

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from environs import Env

from tgbot.services.converter_parser import convert
from tgbot.misc.states import ConverterStates
from tgbot.keyboards.ConverterKeyboards import choose_keyboard

from tgbot.keyboards.callbacks.StartKeyboardsCallback import (
    StartKeyboardsCallback,
)


async def bot_converter_from(call: CallbackQuery, state: FSMContext):
    text = [
        "Выберите из предложенных ниже варинатов валюту для конвертации",
    ]

    await call.message.edit_text("\n".join(text), reply_markup=choose_keyboard)
    await state.set_state(ConverterStates.S1)


async def bot_connverter_to(call: CallbackQuery, state: FSMContext):
    await state.update_data(from_value=call.data.split(":")[1])

    text = [
        "Выберите из предложенных ниже варинатов валюту в которую будем конвертировать",
    ]

    await call.message.edit_text("\n".join(text), reply_markup=choose_keyboard)
    await state.set_state(ConverterStates.S2)


async def bot_connverter_value(call: CallbackQuery, state: FSMContext):
    await state.update_data(to_value=call.data.split(":")[1])

    text = [
        "Введите сумму, которую хотите конвертировать",
    ]

    await call.message.edit_text("\n".join(text))
    await state.set_state(ConverterStates.S3)


async def bot_connverter_convert(message: types.Message, state: FSMContext):
    env = Env()
    env.read_env(".env")

    sum_to_convert = message.text

    if (
        sum_to_convert.replace(",", "", 1).isdigit()
        or sum_to_convert.replace(".", "", 1).isdigit()
    ):
        state_data = await state.get_data()

        convert_data = json.loads(
            await convert(
                state_data.get("to_value"),
                state_data.get("from_value"),
                float(sum_to_convert.replace(",", ".", 1)),
                env.str("API_LAYER_TOKEN"),
            )
        )

        if "error" not in convert_data.keys():
            text = [
                f"При конвертации из {convert_data['from']} в {convert_data['to']} на сумму {convert_data['amount']} {convert_data['from']}",
                f"Вы получите {convert_data['result']} {convert_data['to']}",
                "",
                f"Курс в текущий момент {convert_data['rate']}",
            ]

            await message.answer("\n".join(text))
            await state.finish()

        else:
            text = [
                "Введена неверная сумма",
            ]

            await message.answer("\n".join(text))

    else:
        text = [
            "Введена неверная сумма",
        ]

        await message.answer("\n".join(text))


def register_converter(dp: Dispatcher):
    dp.register_callback_query_handler(
        bot_converter_from, StartKeyboardsCallback.filter(choiсe="converter")
    )
    dp.register_callback_query_handler(bot_connverter_to, state=ConverterStates.S1)
    dp.register_callback_query_handler(bot_connverter_value, state=ConverterStates.S2)
    dp.register_message_handler(bot_connverter_convert, state=ConverterStates.S3)
