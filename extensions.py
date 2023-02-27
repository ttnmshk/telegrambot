import requests
import json
from config import token, keys
import telebot


class ExchangeException(Exception):
    pass

class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ExchangeException(
                f'Невозможно конвертировать одинаковые валюты.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ExchangeException(f'{quote.capitalize()} -- недоступная для конвертации валюта')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ExchangeException(f'{base.capitalize()} -- недоступная для конвертации валюта')

        try:
            amount = int(amount)
        except ValueError:
            raise ExchangeException(f'{amount.capitalize()} -- некорректное значение')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * float(amount)
        return total_base