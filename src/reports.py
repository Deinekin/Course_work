import functools
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd
import pandas as pd
from typing import Callable, Any
from data.config import XLS_PATH, REPORT_FILE
from src.logger import setup_logging

logger = setup_logging()


def report_to_file(*, filename=REPORT_FILE) -> Callable:
    """
    Записываем отчет в файл
    :param filename: название файла
    :return:
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Callable:
            res = func(*args, **kwargs)
            with open(filename, 'w', encoding='utf-8'):
                res.to_excel(filename, index=False)
                logger.info("Данные записаны в файл")
            return res

        return inner

    return wrapper


@report_to_file()
def by_category(df: pd.DataFrame, category_name: str,
                date_: str = dt.now().date().strftime("%d.%m.%Y")) -> pd.DataFrame:
    """
    Смотрим траты по указанной категории за последние 3 месяца с указанной даты
    :param df: Датафрейм, с которым будем работать
    :param category_name: Категория, по которой будет вестись поиск
    :param date_: Дата, от нее отсчитываем 3 месяца назад
    :return: Отфильтрованный датафрейм
    """
    end_date = dt.strptime(date_, '%d.%m.%Y')
    start_date = end_date - rd(months=3)
    # print((dt.strftime(start_date, "%d.%m.%Y")))
    # print((dt.strftime(end_date, "%d.%m.%Y")))

    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True, format="%d.%m.%Y")
    filtered_by_date_df = df.loc[(dt.strftime(start_date, "%d.%m.%Y") < df['Дата платежа']) & (
            df['Дата платежа'] <= dt.strftime(end_date, "%d.%m.%Y"))]
    filtered_by_date_and_category_df = filtered_by_date_df.loc[df['Категория'] == category_name]
    logger.info(f"Получены транзакции за 3 месяца от {date_} по категории {category_name}")
    return filtered_by_date_and_category_df

# print(by_category(pd.read_excel(XLS_PATH), "Супермаркеты", '31.12.2021'))
