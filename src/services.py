import json
import re
from src.utils import list_with_transactions_json
from src.logger import setup_logging

logger = setup_logging()


def filter_by_phone_number(list_with_transactions: list[dict]) -> json:
    """
    Фильтруем транзакции по наличию номера телефона в описании
    :param list_with_transactions: список словарей, полученный из .json
    :return: .json-файл со всеми транзакциями, содержащими в описании мобильные номера
    """
    # return filter(lambda x: "+7" in x['Описание'], list_with_transactions)
    phone_number_filter = list(
        filter(lambda x: bool(re.search(r'[+]?\d \d{1,3}-\d{1,3}-\d{1,3}', x['Описание'])), list_with_transactions))
    logger.info("Получены данные о всех транзакциях с указанными мобильными номерами")
    return json.dumps(phone_number_filter, ensure_ascii=False, indent=4)


def search_by_string(list_with_transactions: list[dict], search_str: str) -> json:
    """
    Возвращаем .json со всеми транзакциями, содержащими запрос в описании или категории
    :param list_with_transactions: список словарей с транзакциями
    :param search_str: запрос поиска
    :return: json со всеми транзакциями, содержащими запрос в описании или категории
    """
    searcher_description = list(
        filter((lambda x: search_str.lower() in x['Описание'].lower()) or search_str.lower() in
               str(x['Категория']).lower(), list_with_transactions))
    logger.info("Получены данные о всех транзакциях с указанной строкой поиска в описании или категории")
    return json.dumps(searcher_description, ensure_ascii=False, indent=4)


def filter_by_individual_transactions(list_with_transactions: list[dict]) -> json:
    """
    Ищем переводы физ. лицам
    :param list_with_transactions: список словарей с транзакциями
    :return: json транзакций, где в описании есть имя и первая буква фамилии с точкой
    """
    filter_by_individuals = list(
        filter(lambda x: bool(re.search(r'[А-Я][а-я]+\s+[А-Я]\.', x['Описание'])) and x['Категория'] == "Переводы",
               list_with_transactions))
    logger.info("Получены данные о всех транзакциях с указанными именем и первой буквой фамилии")
    return json.dumps(filter_by_individuals, ensure_ascii=False, indent=4)

# print(filter_by_phone_number(list_with_transactions_json))
# print(search_by_string(list_with_transactions_json, "яндекс такси"))
# print(filter_by_individual_transactions(list_with_transactions_json))
