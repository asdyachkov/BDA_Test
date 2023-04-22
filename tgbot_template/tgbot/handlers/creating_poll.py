from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.callbacks.StartKeyboardsCallback import StartKeyboardsCallback
from tgbot_template.tgbot.misc.states import CreatingPollStates
from tgbot_template.tgbot.keyboards.CreatingPollKeyboards import *


def isdigit(s):
    if s.startswith("-"):
        s = s[1:]
    return s.isdigit()


async def bot_poll_chat_id(call: CallbackQuery, state: FSMContext):
    text = [
        "Введите chat_id группы, в которую будет отправлено голосование",
        "Не забудте добавить бота в группу, чтобы он мог отправлять сообщения",
    ]

    await call.message.edit_text("\n".join(text))
    await state.set_state(CreatingPollStates.S1)


async def bot_poll_question(message: types.Message, state: FSMContext):
    if isdigit(message.text):
        await state.update_data(chat_id=message.text)
        text = [
            "Введите вопрос, который будет задан при голосовании",
        ]
        await message.answer("\n".join(text))
        await state.set_state(CreatingPollStates.S2)
    else:
        text = [
            "Введенный chat_id неверен",
            "Он должен состоять только из цифр",
            "Например, 123456",
            "Попробуйте еще раз",
        ]
        await message.answer("\n".join(text))


async def bot_poll_answers(message: types.Message, state: FSMContext):
    if 10 <= len(message.text) < 300:
        await state.update_data(question=message.text)
        text = [
            "Через запятую перечислите варианты ответа на голосование",
            "Например: Весна, 123, Да",
            "Минимум 2 варианта ответа от 1 до 100 символов каждый",
            "Максимум - 10 вариантов",
        ]
        await message.answer("\n".join(text))
        await state.set_state(CreatingPollStates.S3)
    else:
        text = [
            "Введенный вопрос неверен",
            "Он должен быть длиннее 10 символов, но короче 300 с учетом пробелов и знаков припинания",
            "Попробуйте еще раз",
        ]
        await message.answer("\n".join(text))


async def bot_poll_is_anonymous(message: types.Message, state: FSMContext):
    answers = [answer for answer in message.text.split(",") if len(str(answer)) >= 1]
    if 1 < len(answers) <= 10:
        await state.update_data(answers=answers)
        text = [
            "Ответьте на клавиатуре, будет ли опрос анономным?",
            "Обратите внимание, что если вы хотите отправить опрос в группуЮ он должен быть анонимным",
        ]
        await message.answer("\n".join(text), reply_markup=is_poll_anonymous)
        await state.set_state(CreatingPollStates.S4)
    else:
        text = [
            "Введенные варианты ответов не удовлетворяют указанным условиям",
            "Через запятую перечислите варианты ответа на голосование",
            "Например: Весна, 123, Да",
            "Минимум 2 варианта ответа от 1 до 100 символов каждый",
            "Максимум - 10 вариантов",
        ]
        await message.answer("\n".join(text))


async def bot_poll_open_period(call: CallbackQuery, state: FSMContext):
    await state.update_data(is_anonymous=call.data.split(":")[1])
    text = [
        "Введите время в секундных сколько будет доступно голосование",
        "Введите целое число от 5 до 600 - количество секунд",
    ]
    await call.message.answer("\n".join(text))
    await state.set_state(CreatingPollStates.S5)


async def bot_poll_type(message: types.Message, state: FSMContext):
    open_period = message.text
    if open_period.strip().isdigit():
        open_period = int(open_period.strip())
        if 5 <= open_period <= 600:
            await state.update_data(open_period=open_period)
            text = [
                "Выберите на клавиатуре нужный тип голосования",
                "Quiz - 1 правильный ответ",
                "Regular - правильного ответа нет",
            ]
            await message.answer("\n".join(text), reply_markup=poll_type)
            await state.set_state(CreatingPollStates.S6)
        else:
            text = [
                "Введено неверное число",
                "Введите целое число от 5 до 600 - количество секунд",
            ]
            await message.answer("\n".join(text))
    else:
        text = [
            "Введено неверное число",
            "Введите целое число от 5 до 600 - количество секунд",
        ]
        await message.answer("\n".join(text))


async def bot_poll_correct_type_or_allows_multiple_answers(
    call: CallbackQuery, state: FSMContext
):
    type_ = call.data.split(":")[1]
    await state.update_data(type=type_)
    if type_ == "quiz":
        data = await state.get_data()
        text = [
            "Выберите на клавиатуре правильный ответ на голосование",
        ]
        await call.message.answer(
            "\n".join(text), reply_markup=correct_type(data["answers"])
        )
        await state.set_state(CreatingPollStates.S61)
    else:
        text = [
            "Выберите на клавиатуре, разрешен ли выбор нескольких вариантов в голосовании",
        ]
        await call.message.answer(
            "\n".join(text), reply_markup=is_allows_multiple_answers
        )
        await state.set_state(CreatingPollStates.S62)


async def bot_poll_explanation(call: CallbackQuery, state: FSMContext):
    await state.update_data(correct_option_id=call.data.split(":")[1])
    text = [
        "Введите текстовое пояснение, которое будет появляться при выборе неправильного варанта ответа",
        "Максимальная длина сообщения - 200 символов",
    ]
    await call.message.answer("\n".join(text))
    await state.set_state(CreatingPollStates.S611)


async def get_explanation(message: types.Message, state: FSMContext):
    explanation = message.text
    if len(explanation) < 200:
        await state.update_data(explanation=explanation)
        try:
            data = await state.get_data()
            await message.bot.send_poll(
                chat_id=data.get("chat_id"),
                question=data.get("question"),
                options=data.get("answers"),
                is_anonymous=data.get("is_anonymous"),
                type=data.get("type"),
                correct_option_id=data.get("correct_option_id"),
                explanation=data.get("explanation"),
                open_period=data.get("open_period"),
            )
            text = [
                "Голосование отправлено по указанному id",
            ]
        except Exception as e:
            text = [
                f"Голосование не отправлено по указанному id",
                f"Возникла ошибка: {e}",
            ]
        await message.answer("\n".join(text))
        await state.finish()
    else:
        text = [
            "Введенное сообщение не удовлетворяет условиям",
            "Попробуйте еще раз",
            "Максимальная длина сообщения - 200 символов",
        ]
        await message.answer("\n".join(text))


async def get_allows_multiple_answers(call: CallbackQuery, state: FSMContext):
    await state.update_data(allows_multiple_answers=call.data.split(":")[1])
    try:
        try:
            data = await state.get_data()
            await call.message.bot.send_poll(
                chat_id=data.get("chat_id"),
                question=data.get("question"),
                options=data.get("answers"),
                is_anonymous=data.get("is_anonymous"),
                type=data.get("type"),
                allows_multiple_answers=data.get("allows_multiple_answers"),
                open_period=data.get("open_period"),
            )
            text = [
                "Голосование отправлено по указанному id",
            ]
        except Exception as e:
            text = [
                f"Голосование не отправлено по указанному id",
                f"Возникла ошибка: {e}",
            ]
        await call.message.answer("\n".join(text))
        await state.finish()
    except Exception as e:
        text = [
            f"Возникла ошибка: {e}",
        ]
        await call.message.answer("\n".join(text))


def register_creating_poll(dp: Dispatcher):
    dp.register_callback_query_handler(
        bot_poll_chat_id, StartKeyboardsCallback.filter(choiсe="create_poll")
    )
    dp.register_message_handler(bot_poll_question, state=CreatingPollStates.S1)
    dp.register_message_handler(bot_poll_answers, state=CreatingPollStates.S2)
    dp.register_message_handler(bot_poll_is_anonymous, state=CreatingPollStates.S3)
    dp.register_callback_query_handler(
        bot_poll_open_period, state=CreatingPollStates.S4
    )
    dp.register_message_handler(bot_poll_type, state=CreatingPollStates.S5)
    dp.register_callback_query_handler(
        bot_poll_correct_type_or_allows_multiple_answers, state=CreatingPollStates.S6
    )
    dp.register_callback_query_handler(
        bot_poll_explanation, state=CreatingPollStates.S61
    )
    dp.register_message_handler(get_explanation, state=CreatingPollStates.S611)
    dp.register_callback_query_handler(
        get_allows_multiple_answers, state=CreatingPollStates.S62
    )
