# FSC/wrappers.py
import xmltodict
import datetime

from functools import reduce

# from core.validators import isolate_params
# from core.wrapper_decorators import required_kwargs, recommended_kwargs
# from core.env_functions import get_dotenv, get_env_variable, get_env_variable_list

from .API import BaseFSCAPI

get_dotenv("FSC.env")
FSC_key = get_env_variable("Key")

fsc = FSCPaginatorAPI(
    APIKey = FSC_key
)



@recommended_kwargs(["basDt"])
def getBondData(**kwargs):
    """
    gets Issued Bond Data from FSC
    https://www.data.go.kr/data/15059592/openapi.do
    """

    fsc.set_path("/GetBondIssuInfoService/getBondBasiInfo")
    fsc.set_return_type("xml")
    fsc.skip_validation = True

    non_iterator_params = isolate_params(
        needed_kwargs = ["basDt", "numOfRows", "pageNo"],
        kwargs = kwargs
    )

    fsc._set_paginator_params(**iterator_params)

    bond_data_list = list()
    ret = True
    for (ret, r) in fsc:
        bond_data_list.append(
            r["response"]["body"]["items"]
        )
