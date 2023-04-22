import json
import logging

from aiohttp import ClientSession


async def cat_photo() -> json:
    """
    Асинхронный парсер котиков
    :return: json
    """
    try:
        async with ClientSession() as session:
            async with session.get(
                url="https://api.thecatapi.com/v1/images/search"
            ) as response:
                data_json = await response.json()
                cat_url = data_json[0]["url"]
                json_to_return = json.dumps(
                    {
                        "cat_url": cat_url,
                    }
                )

    except Exception as ex:
        json_to_return = json.dumps(
            {
                "error": "Возникла ошибка",
            }
        )
        logging.error(ex)
    return json_to_return
