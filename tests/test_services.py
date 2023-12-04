import json
import pytest
from src.services import search_by_string, filter_by_individual_transactions, filter_by_phone_number


@pytest.fixture()
def transactions_data():
    return [
        {
            "Дата операции": "27.02.2018 23:17:40",
            "Дата платежа": "28.02.2018",
            "Номер карты": 0,
            "Статус": "OK",
            "Сумма операции": -100.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -100.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 0.0,
            "Категория": "Мобильная связь",
            "МСС": 0.0,
            "Описание": "Я МТС +7 921 11-22-33",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 100.0
        },
        {
            "Дата операции": "11.01.2018 00:00:00",
            "Дата платежа": "13.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -94.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -94.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 0.0,
            "Категория": "Транспорт",
            "МСС": 4121.0,
            "Описание": "Яндекс Такси",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 94.0
        },
        {
            "Дата операции": "17.01.2018 13:24:11",
            "Дата платежа": "17.01.2018",
            "Номер карты": 0,
            "Статус": "OK",
            "Сумма операции": -4350.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -4350.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 0.0,
            "Категория": "Переводы",
            "МСС": 0.0,
            "Описание": "Иван Ф.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 4350.0
        }
    ]


def test_filter_by_phone_number(transactions_data):
    assert json.loads(filter_by_phone_number(transactions_data))[0] == {
        "Дата операции": "27.02.2018 23:17:40",
        "Дата платежа": "28.02.2018",
        "Номер карты": 0,
        "Статус": "OK",
        "Сумма операции": -100.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -100.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": 0.0,
        "Категория": "Мобильная связь",
        "МСС": 0.0,
        "Описание": "Я МТС +7 921 11-22-33",
        "Бонусы (включая кэшбэк)": 1,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 100.0
    }


def test_search_by_string(transactions_data):
    assert json.loads(search_by_string(transactions_data, "Яндекс Такси"))[0] == {
        "Дата операции": "11.01.2018 00:00:00",
        "Дата платежа": "13.01.2018",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -94.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -94.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": 0.0,
        "Категория": "Транспорт",
        "МСС": 4121.0,
        "Описание": "Яндекс Такси",
        "Бонусы (включая кэшбэк)": 1,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 94.0
    }


def test_filter_by_individual_transactions(transactions_data):
    assert json.loads(filter_by_individual_transactions(transactions_data))[0] == {
        "Дата операции": "17.01.2018 13:24:11",
        "Дата платежа": "17.01.2018",
        "Номер карты": 0,
        "Статус": "OK",
        "Сумма операции": -4350.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -4350.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": 0.0,
        "Категория": "Переводы",
        "МСС": 0.0,
        "Описание": "Иван Ф.",
        "Бонусы (включая кэшбэк)": 0,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 4350.0
    }
