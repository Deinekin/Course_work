import pytest

from src.views import get_card, get_cards_spends_and_cashback, filter_by_date, get_top_five_spends


def test_get_card():
    assert get_card('12345125') == '5125'


@pytest.fixture()
def get_list_dict():
    return filter_by_date("2021-12-01 12:36:08")


def test_filter_by_date(get_list_dict):
    assert get_list_dict[0] == {'Дата операции': '01.12.2021 12:35:05',
                                'Дата платежа': '01.12.2021', 'Номер карты': '*7197',
                                'Статус': 'OK', 'Сумма операции': -99.0,
                                'Валюта операции': 'RUB',
                                'Сумма платежа': -99.0, 'Валюта платежа': 'RUB', 'Кэшбэк': 0.0,
                                'Категория': 'Фастфуд', 'МСС': 5814.0,
                                'Описание': 'IP Yakubovskaya M.V.',
                                'Бонусы (включая кэшбэк)': 1,
                                'Округление на инвесткопилку': 0,
                                'Сумма операции с округлением': 99.0}


def test_get_cards_spends_and_cashback(get_list_dict):
    assert get_cards_spends_and_cashback(get_list_dict)[0] == {'last_digits': '7197', 'total_spent': 99.0,
                                                               'cashback': 0.99}


def test_get_top_five_spends(get_list_dict):
    assert get_top_five_spends(get_list_dict)[0] == {'date': '01.12.2021', 'amount': 99.0, 'category': 'Фастфуд',
                                                     'description': 'IP Yakubovskaya M.V.'}
