from aiogram.dispatcher.filters.state import StatesGroup, State

# Файл с машинами состояний для каждого из хендлеров


class WeatherStates(StatesGroup):
    S1 = State()


class ConverterStates(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()


class CreatingPollStates(StatesGroup):
    S1 = State()
    S2 = State()
    S3 = State()
    S4 = State()
    S5 = State()
    S6 = State()
    S61 = State()
    S62 = State()
    S611 = State()
    S621 = State()
    S612 = State()
    S622 = State()
