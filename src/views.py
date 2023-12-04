import json
import os
from datetime import timedelta, datetime as dt
from src.utils import list_with_transactions_json
import pandas as pd
import requests
from data.config import USER_SETTINGS
from dotenv import load_dotenv
from src.logger import setup_logging

logger = setup_logging()


def greeting() -> str:
    """
    Приветствие в зависимости от времени суток
    :return: Строка с приветствием
    """
    current_hour = dt.now().hour
    if current_hour <= 3:
        return "Добрая ночь!"
    if current_hour <= 11:
        return "Доброе утро!"
    if current_hour <= 16:
        return "Добрый день!"
    logger.info("Выполнено приветствие пользователя")
    return "Добрый вечер!"


def get_card(card: str) -> str:
    """
    Возвращает последние 4 цифры карты
    :param card: карта или ее маска
    :return: последние 4 цифры
    """
    logger.info("Получены последние 4 цифры номера карты")
    return card[-4:]


def filter_by_date(date_and_time: str) -> list[dict]:
    """
    По указанной дате из данных эксель файла, преобразованных в список словарей, отфильтровываем операции
    с начала месяца до указанной даты
    :param date_and_time: дата и время
    :return: список словарей с начала месяца до указанной даты
    """
    date_ = (f'{date_and_time[8:10]}.{date_and_time[5:7]}.{date_and_time[:4]} '
             f'{date_and_time[11:13]}:{date_and_time[14:16]}:{date_and_time[17:19]}')
    end_date = dt.strptime(date_, '%d.%m.%Y %H:%M:%S')
    start_date = end_date - timedelta(end_date.day - 1, hours=end_date.hour, minutes=end_date.minute,
                                      seconds=end_date.second)

    new_list = [x for x in list_with_transactions_json if
                start_date <= dt.strptime(x['Дата операции'], '%d.%m.%Y %H:%M:%S') <= end_date and x[
                    'Сумма операции'] < 0 and x['Номер карты'] != 0]
    logger.info(f"Получены все транзакции от {start_date} до {end_date}")
    return new_list


def get_cards_spends_and_cashback(list_: list[dict]):
    """
    Получаем отчет по картам, на каких картах какие траты и сколько кэшбэка нам за это отдадут
    :param list_: список словарей
    :return: список словарей с последними 4 цифрами карты, тратами по картам и кэшбэку
    """
    df: pd.DataFrame = pd.DataFrame(list_)
    grouped_by_card = -df.groupby('Номер карты')['Сумма операции'].sum()
    # print(type(grouped_by_card))
    list_dict = []
    for index, item in grouped_by_card.items():
        dict_ = {"last_digits": get_card(index),
                 "total_spent": item,
                 "cashback": round(item / 100, 2)}
        list_dict.append(dict_)
    logger.info("Получены данные по карте, тратам за указанный период времени и кэшбэку")
    return list_dict


def get_top_five_spends(list_: list[dict]) -> list[dict]:
    """
    Смотрим топ-5 трат
    :param list_: список словарей
    :return: список словарей с датой платежа, суммой операции, категорией и описанием
    """
    df = pd.DataFrame(list_)
    sorted_df: pd.DataFrame = df.sort_values('Сумма операции', ascending=True)
    top_transactions_list = sorted_df.head()
    # print(type(top_transactions_list))
    res_list = []
    for row in top_transactions_list.iterrows():
        dict_ = {"date": row[1]['Дата платежа'],
                 "amount": -row[1]['Сумма операции'],
                 "category": row[1]['Категория'],
                 "description": row[1]['Описание']}
        res_list.append(dict_)
    # print(res_list)
    logger.info("Получены наибольшие 5 трат за указанный период времени")
    return res_list


def get_currencies(user_currencies: list) -> list[dict]:
    """
    Получаем актуальные курсы валют
    :param user_currencies: список валют, которые хочет посмотреть пользователь
    :return: список словарей с валютами и их курсом
    """
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    res_list = []
    for currency in user_currencies:
        dict_ = {'currency': currency,
                 "rate": round(response['Valute'][currency]['Value'], 2)}
        res_list.append(dict_)
    logger.info("Получены актуальные курсы валют")
    return res_list


def get_stocks(user_stocks: list) -> list[dict]:
    """
    Получаем актуальные курсы акций
    :param user_stocks: список акций, которые интересны пользователю
    :return: список словарей, состоящий из акций и их стоимости в рублях
    """
    res_list = []
    load_dotenv()
    api_key = os.getenv("API_KEY")

    with open(USER_SETTINGS) as f:
        res = json.load(f)
    currencies = get_currencies(res["user_currencies"])

    for stock in user_stocks:
        url = f'https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}'
        response = requests.get(url).json()
        dict_ = {"stock": stock,
                 "price": round(response['c'] * currencies[0]["rate"], 2)}
        res_list.append(dict_)
    logger.info("Получены актуальные курсы акций в рублях")
    return res_list


def get_data_from_user_settings(filepath: str) -> dict:
    """
    Получаем данные из настроек пользователя
    :param filepath: путь до файла
    :return: список словарей с настройками пользователя
    """
    with open(filepath) as f:
        user_data = json.load(f)
    return user_data


def make_json_report(date_and_time: str) -> json:
    """
    Итоговая функция. Собираем все в словарь, а словарь переводим в .json
    :param date_and_time: дата и время в формате "YYYY-MM-DD HH:MM:SS"
    :return: .json-файл со всеми интересующими нас данными
    """
    # Здороваемся
    greeting_message = greeting()
    # Фильтруем данные от начала месяца до текущей даты
    data_from_months_starts = filter_by_date(date_and_time)
    # Получаем список словарей - на каких картах сколько потратили и сколько вернется
    spends_and_cashback = get_cards_spends_and_cashback(data_from_months_starts)
    # Смотрим, на что мы потратили за это время больше всего денег
    top_five_spends = get_top_five_spends(data_from_months_starts)
    # Берем данные из .json файла с настройками пользователя
    user_settings_data = get_data_from_user_settings(USER_SETTINGS)
    # Получаем курсы валют, исходя из требований пользователя
    currencies_rate = get_currencies(user_settings_data['user_currencies'])
    # Получаем курсы акций в рублях из S&P500, исходя из требований пользователя
    stocks_rate = get_stocks(user_settings_data['user_stocks'])
    # Запихиваем все в словарь
    res_dict = {"greeting": greeting_message,
                "cards": spends_and_cashback,
                "top_transactions": top_five_spends,
                "currencies_rate": currencies_rate,
                "stock_prices": stocks_rate}
    # Запихиваем словарь в .json
    logger.info("Создана форма отчета в формате .json")
    return json.dumps(res_dict, ensure_ascii=False, indent=4)


# print(make_json_report("2020-12-02 16:45:08"))
