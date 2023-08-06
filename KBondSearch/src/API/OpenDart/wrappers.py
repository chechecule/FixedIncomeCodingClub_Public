# OpenDart.wrappers.py

import json

from core.wrapper_decorators import required_kwargs, recommended_kwargs
from BaseFunctions.env_functions import get_dotenv, get_env_variable, get_env_variable_list

from .wrappers_base import opendart, opendartpaginator, corp_code_from_stock_code


##########################################################################################################
##############################   전체 재무제표  ###########################################################
##########################################################################################################


opendart.skip_validation = False


@required_kwargs(["corp_code", "bsns_year", "reprt_code", "fs_div"])
def get_corp_financial_data_all(corp_code, bsns_year, reprt_code, fs_div):
    """
    Gets financial data of corporate code
    year : "yyyy",
    reprt_code =
        1분기보고서 : 11013
        반기보고서 : 11012
        3분기보고서 : 11014
        사업보고서 : 11011

    https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020
    """
    opendart.set_path("fnlttSinglAcntAll")
    opendart.set_return_type("json")


    ret, r = opendart.read(
        corp_code = str(corp_code),
        bsns_year = bsns_year,
        reprt_code = reprt_code,
        fs_div = fs_div,
    )

    return ret, r.json()


def get_corp_financial_all_by_stock_code(stock_code, **kwargs):
    corp_code = corp_code_from_stock_code(stock_code)

    return get_corp_financial_data_all(corp_code=corp_code, **kwargs)

##########################################################################################################
##############################  주요 재무제표  ###########################################################
##########################################################################################################

@required_kwargs(["corp_code", "bsns_year", "reprt_code"])
def get_corp_financial_main(corp_code, bsns_year, reprt_code):
    """
    Gets financial data of corporate code
    year : "yyyy",
    reprt_code =
        1분기보고서 : 11013
        반기보고서 : 11012
        3분기보고서 : 11014
        사업보고서 : 11011

    https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020
    """
    opendart.set_path("fnlttSinglAcnt")
    opendart.set_return_type("json")

    ret, r = opendart.read(
        corp_code = str(corp_code),
        bsns_year = bsns_year,
        reprt_code = reprt_code,
    )
    return ret, r.json()


def get_corp_financial_main_by_stock_code(stock_code, **kwargs):
    corp_code = corp_code_from_stock_code(stock_code)
    return get_corp_financial_data_all(corp_code=corp_code, **kwargs)