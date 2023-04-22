import json
import logging

from aiohttp import ClientSession

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B",
}  # От парсера приходят значения, которые можно преобразовать в эмодзи


async def get_weather(city: str, open_weather_token: str) -> json:
    """
    Асинхронный парсер погоды
    :param city: город для парсинга
    :param open_weather_token: токен для апи
    :return: json
    """
    try:
        async with ClientSession() as session:
            async with session.get(
                url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
            ) as response:
                weather = await response.json()
                city = weather["name"]
                current_temperature = weather["main"]["temp"]
                current_humidity = weather["main"]["humidity"]
                current_pressure = weather["main"]["pressure"]
                current_wind_speed = weather["wind"]["speed"]
                weather_description = weather["weather"][0]["main"]
                if weather_description in code_to_smile:
                    wd = code_to_smile[weather_description]
                else:
                    wd = "Картинки на происходящее у меня нет..."
                json_to_return = json.dumps(
                    {
                        "city": city,
                        "current_temperature": current_temperature,
                        "current_humidity": current_humidity,
                        "current_pressure": current_pressure,
                        "current_wind_speed": current_wind_speed,
                        "weather_description": wd,
                    }
                )

    except Exception as ex:
        json_to_return = json.dumps(
            {
                "error": "Проверьте правильность введенного города",
            }
        )
        logging.error(ex)
    return json_to_return
