# OpenDart/wrappers_base.py

import json
import pandas as pd

from cachetools import cached, TTLCache

from BaseFunctions.env_functions import get_dotenv, get_env_variable, get_env_variable_list
from core.wrapper_decorators import required_kwargs, recommended_kwargs

from .API import OpenDartAPI, OpenDartPaginaterAPI

cache = TTLCache(maxsize=100, ttl=10000)

get_dotenv("opendart.env")
dart_keys = get_env_variable_list("OPENDART_LIST")

opendart = OpenDartAPI(
    APIKey = dart_keys[0],
    APIList = dart_keys
    )

opendartpaginator = OpenDartPaginaterAPI(
    APIKey = dart_keys[0],
    APIList = dart_keys
    )

@cached(cache)
def get_corp_code():
    """
    Downloads zip file containing code data and converts into dataframe
    """
    opendart.set_path("corpCode")
    opendart.set_return_type("xml")
    opendart.skip_validation = True

    ret, r = opendart.read()

    if ret:
        # fead the data to the zip_file opener
        data = opendart.open_zip_file(r.content, "CORPCODE.xml")

        df = pd.DataFrame(data['result']['list'])
        return ret, df

    return ret, r

def stock_corp_code():
    """
    Filters corp code data to only have codes enlisted in the stock market
    """
    ret, df = get_corp_code()

    if ret:
        return ret, df[df['stock_code'].notna()]

    else:
        raise ValueError("stock_corp_code did not load")


def corp_code_from_stock_code(stock_code):

    ret, df = stock_corp_code()
 

    df = stock_corp_code[
        stock_corp_code_df["stock_code"] == str(stock_code)
        ]
    if not df.empty:
        corp_code = df["corp_code"].values[0]
        return corp_code

    else:
        raise ValueError(f"{stock_code} does not exit")

@required_kwargs(["corp_code"])
def get_corp_summary(corp_code):
    """
    Returns corporate summary.
    https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002
    """
    opendart.set_path("company")
    opendart.set_return_type("json")
    opendart.skip_validation = False

    ret, r = opendart.read(
        corp_code = str(corp_code)
    )

    return ret, r.json()

def get_corp_summary_by_stock_code(stock_code):
    """
    Gets company summary by stock code
    """

    return get_corp_summary(corp_code_from_stock_code(stock_code))

