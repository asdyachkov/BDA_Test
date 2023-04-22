import json
import logging

from aiohttp import ClientSession


async def convert(
    to_value: str = "USD",
    from_value: str = "RUB",
    amount: float = 100,
    api_layer_token: str = None,
) -> json:
    try:
        async with ClientSession() as session:
            headers = {"apikey": api_layer_token}
            async with session.get(
                url=f"https://api.apilayer.com/fixer/convert?to={to_value}&from={from_value}&amount={amount}",
                headers=headers,
            ) as response:
                converted = await response.json()
                json_to_return = json.dumps(
                    {
                        "result": converted["result"],
                        "rate": converted["info"]["rate"],
                        "amount": converted["query"]["amount"],
                        "from": converted["query"]["from"],
                        "to": converted["query"]["to"],
                    }
                )

    except Exception as ex:
        json_to_return = json.dumps(
            {
                "error": "Проверьте правильность введенной суммы",
            }
        )
        logging.error(ex)
    return json_to_return
