# FSC/wrappers.pye
import pandas as pd

from functools import reduce

from API.core.validators import isolate_params
from API.core.wrapper_decorators import required_kwargs, recommended_kwargs
from API.core.env_functions import get_dotenv, get_env_variable, get_env_variable_list

# from utils.time_functions import random_sleep

from .API import FSCPaginatorAPI



#FSC_key = "bCvxIs2OB+YwCRrOBw2Ca0bL483bA1VzGHf1w55JpEurqqu7WMWdH+uvJJtcmUTJOGK+i/8avBJT+aldq/kozg=="
get_dotenv("FSC.env")
FSC_key = get_env_variable("Key")

fsc = FSCPaginatorAPI(
    APIKey = FSC_key
)
#paginator에서 fsc 키를 넣고 실행

@recommended_kwargs(["basDt"])
def getBondData(**kwargs) -> pd.DataFrame:
    """
    gets Issued Bond Data from FSC
    https://www.data.go.kr/data/15043421/openapi.do
    """

    fsc.set_path("/1160100/service/GetBondTradInfoService/getIssuIssuItemStat")
    fsc.set_return_type("json")
    fsc.skip_validation = True

    kwargs = {"numOfRows" : 15, "pageNo" : 1, "basDt" : kwargs.get("basDt")}
    #100개를 한번에 가져오고 page no 1부터 시작. 기준일자는 따로 지정


    iterator_params = isolate_params(
        needed_kwargs = ["basDt", "numOfRows", "pageNo"],
        kwargs = kwargs
    )
    #이게 있나 기본적으로 확인하는 작업인듯


    fsc.initialize_params_for_iterator(**iterator_params)
    fsc._set_paginator_params()
    # 지정안되되어있으면 여기서 지정

#결국 여기밑에서 가져오는것
    bond_data_list = list()

    for (ret, r) in fsc:

#from tqdm import tqdm
#tqdmrnage
## 반복문을 통해 fsc의 요소들을 하나씩 가져와서 ret과 r로 언패킹
        bond_data_list.extend(r["response"]["body"]["items"]["item"])
    return pd.DataFrame(bond_data_list)
