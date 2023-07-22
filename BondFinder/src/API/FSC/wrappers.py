# FSC/wrappers.py
import xmltodict
import datetime
import pandas as pd
from functools import reduce

from API.core.validators import isolate_params
from API.core.wrapper_decorators import required_kwargs, recommended_kwargs
from API.core.env_functions import get_dotenv, get_env_variable, get_env_variable_list

from utils.time_functions import random_sleep

from FSC.API import FSCPaginatorAPI




get_dotenv("FSC.env")
FSC_key = get_env_variable("Key")

fsc = FSCPaginatorAPI(
    APIKey = FSC_key
)




@recommended_kwargs(["basDt"])
def getBondData(**kwargs) -> pd.DataFrame:
    """
    gets Issued Bond Data from FSC
    https://www.data.go.kr/data/15059592/openapi.do
    """

    fsc.set_path("/1160100/service/GetBondIssuInfoService/getBondBasiInfo")
    fsc.set_return_type("xml")
    fsc.skip_validation = True

    kwargs = {"numOfRows" : 2, "pageNo" : 1, "basDt" : 20200409}

    non_iterator_params = isolate_params(
        needed_kwargs = ["basDt", "numOfRows", "pageNo"],
        kwargs = kwargs
    )


    fsc.initialize_params_for_iterator(**non_iterator_params)
    fsc._set_paginator_params()

    bond_data_list = list()

    for (ret, r) in fsc:
        bond_data_list.append(r["response"]["body"]["items"]["item"])
        random_sleep(1, 5)

    return pd.DataFRame(bond_data_list)
