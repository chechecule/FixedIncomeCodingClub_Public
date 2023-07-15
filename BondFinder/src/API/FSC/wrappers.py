# FSC/wrappers.py
import xmltodict

from core.wrapper_decorators import required_kwargs, recommended_kwargs
from BaseFunctions.env_functions import get_dotenv, get_env_variable, get_env_variable_list

from .wrappers_base import opendart, opendartpaginator, corp_code_from_stock_code