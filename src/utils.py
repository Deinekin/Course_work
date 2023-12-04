import pandas as pd
from data.config import XLS_PATH
from src.logger import setup_logging

logger = setup_logging()


def set_dict(row_of_file: list) -> dict:
    """
    Заполняет словарь элементами списка, состоящего из данных о транзакции
    :param row_of_file: строка из .xls файла с данными о транзакции
    :return: словарь, значениями которого являются элементы поданного на вход списка
    """
    return {
        "Дата операции": row_of_file[0],
        "Дата платежа": row_of_file[1],
        "Номер карты": row_of_file[2],
        "Статус": row_of_file[3],
        "Сумма операции": row_of_file[4],
        "Валюта операции": row_of_file[5],
        "Сумма платежа": row_of_file[6],
        "Валюта платежа": row_of_file[7],
        "Кэшбэк": row_of_file[8],
        "Категория": row_of_file[9],
        "МСС": row_of_file[10],
        "Описание": row_of_file[11],
        "Бонусы (включая кэшбэк)": row_of_file[12],
        "Округление на инвесткопилку": row_of_file[13],
        "Сумма операции с округлением": row_of_file[14],
    }


def read_xls_file(file: str) -> list[dict]:
    """
    Считываем .xlsx файл, данные грузим в словарь, создаем из словарей список
    :param file: путь до .xlsx файла
    :return: список словарей с данными о транзакциях
    """
    list_of_transactions_from_file: list = []
    df: pd.DataFrame = pd.read_excel(file)
    new_df: pd.DataFrame = df.fillna(0)
    for row in new_df.iterrows():
        list_of_transactions_from_file.append(set_dict(row[1].to_list()))
    logger.info("Создана структура, содержащая в себе данные из .xls файла")
    return list_of_transactions_from_file


list_with_transactions_json: list[dict] = read_xls_file(XLS_PATH)
