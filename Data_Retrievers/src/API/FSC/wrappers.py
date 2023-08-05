# FSC/wrappers.pye
import pandas as pd
from functools import reduce

from API.core.validators import isolate_params
from API.core.wrapper_decorators import required_kwargs, recommended_kwargs
from API.core.env_functions import get_dotenv, get_env_variable, get_env_variable_list

# from utils.time_functions import random_sleep

from .API import FSCPaginatorAPI



FSC_key = "bCvxIs2OB+YwCRrOBw2Ca0bL483bA1VzGHf1w55JpEurqqu7WMWdH+uvJJtcmUTJOGK+i/8avBJT+aldq/kozg=="
#get_dotenv("FSC.env")
#FSC_key = get_env_variable("Key")

fsc = FSCPaginatorAPI(
    APIKey = FSC_key
)


@recommended_kwargs(["basDt"])
def getBondData(**kwargs) -> pd.DataFrame:
    """
    gets Issued Bond Data from FSC
    https://www.data.go.kr/data/15043421/openapi.do
    """

    '''
    fsc.set_path("/1160100/service/GetBondIssuInfoService/getBondBasiInfo")
    이전 path
    '''

    fsc.set_path("/1160100/service/GetBondTradInfoService/getIssuIssuItemStat")

    fsc.set_return_type("json")
    fsc.skip_validation = True

    kwargs = {"numOfRows" : 100, "pageNo" : 1, "basDt" : kwargs.get("basDt")}
    #100개를 한번에 가져오고 page no 1부터 시작. 기준일자는 따로 지정


    non_iterator_params = isolate_params(
        needed_kwargs = ["basDt", "numOfRows", "pageNo"],
        kwargs = kwargs
    )
    #이게 있나 기본적으로 확인하는 작업인듯


    fsc.initialize_params_for_iterator(**non_iterator_params)
    fsc._set_paginator_params()

    bond_data_list = list()

    for (ret, r) in fsc:
        bond_data_list.extend(r["response"]["body"]["items"]["item"])

    return pd.DataFrame(bond_data_list)
