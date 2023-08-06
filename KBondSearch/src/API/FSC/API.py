# FSC/API.py



#https://www.data.go.kr/data/15043421/openapi.do
#https://www.data.go.kr/data/15059592/openapi.do
#https://www.data.go.kr/data/15094784/openapi.do

import requests
import pandas as pd


from API.core.singleton_class import SingletonInstance

from API.core.webAPI import BaseOpenAPI
from API.core.validators import response_is_200, is_xml

from .paginators import FSCAPIPaginatorMixin

#https://api.data.go.kr/1160100/GetBondSecuritiesInfoService/getBondPriceInfo?

class BaseFSCAPI(BaseOpenAPI):
    """
    We assume the data returned to be in json.
    This allows to easy use by extending our Postgres database by seeting JSON field
    saving raw data.
    """

    validators = [response_is_200, is_xml]

    def __init__(self, APIKey, *args, **kwargs):
        super().__init__(APIKey, *args, **kwargs)

    def set_path(self, path =""):
        self.path = path

    def set_return_type(self, return_type="xml"):
        self._return_type = return_type

    def return_type(self):
        return getattr(self, "_return_type", "xml")

    @property
    def url(self):
        return "http://apis.data.go.kr" + self.path

    def _add_params(self, **params):

        params.update(
            {
            "serviceKey" : self.APIKey,
            "resultType" : self.return_type()
            }
        )
        return params

    def read(self, url = None, **params):
        return self.get(
            content_type=self.return_type(),
            **params
        )


class FSCPaginatorAPI(BaseFSCAPI , FSCAPIPaginatorMixin):
    pass