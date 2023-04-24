import requests
from translate import Translator


def get_result(number):
    """Получаем случайный факт по числу побед."""
    url = f'http://numbersapi.com/{number}'

    response = requests.get(url).text

    translator = Translator(to_lang="ru")

    result = translator.translate(response)
    return result

