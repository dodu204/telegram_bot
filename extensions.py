import json

import requests

from config import banknotes


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            base_key = banknotes[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        try:
            sym_key = banknotes[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты, {quote}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество, {amount}!')

        headers = {
            "apikey": "GfL5i7Zxc92iryIqag5ahHgun62VKRZX"
        }

        r = requests.get(
            f'https://api.apilayer.com/exchangerates_data/convert?to={banknotes[base]}&from={banknotes[quote]}&amount={amount}',
            headers=headers)
        new_price = round(json.loads(r.content)["result"], 3)
        message = f"Цена {amount} {quote} в {base} - {new_price}"
        return message
