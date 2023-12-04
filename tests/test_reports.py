from src.reports import by_category
from data.config import XLS_PATH
import pandas as pd


def test_by_category():
    df = by_category(pd.read_excel(XLS_PATH), "Супермаркеты", '31.12.2021')
    assert df.shape[0] == 133
