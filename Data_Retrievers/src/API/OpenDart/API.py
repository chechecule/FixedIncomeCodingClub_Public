# OpenDart/API.py

# add logger class later on!
import requests
import pandas as pd
import io
import xmltodict
import zipfile

from core.singleton_class import SingletonInstance

from core.webAPI import BaseOpenAPI
from core.file_handler import BaseFileHandlerMixin
from core.validators import is_json, response_is_200

from .paginators import OpenDartAPIPaginatorMixin
from .validators import success_code_in_header, api_limit_reached




class BaseOpenDartAPI(BaseOpenAPI):
    """
    We assume the data returned to be in json.
    This allows to easy use by extending our Postgres database by seeting JSON field
    saving raw data.
    """

    validators = [success_code_in_header,]

    def __init__(self, APIKey, *args, **kwargs):
        super().__init__(APIKey, *args, **kwargs)

    def set_path(self, path =""):
        self.path = path

    def set_return_type(self, return_type="json"):
        self._return_type = return_type

    def return_type(self):
        return getattr(self, "_return_type", "json")

    @property
    def url(self):
        return "https://opendart.fss.or.kr/api/" + self.path + f".{self.return_type()}?"

    def _add_params(self, **params):
        params.update(
            {"crtfc_key" : self.APIKey}
        )
        return params

    def read(self, url = None, **params):
        return self.get(
            content_type=self.return_type(),
            **params
        )


class BaseOpenDartMultipleAPI(BaseOpenDartAPI):
    """
    Since OpenDart API allows 10,000 requests per day, we create a
    multiple API handler mixin to offer an automatic API Key switching
    functionality
    """

    api_switch_event_conditions = [api_limit_reached, ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.APIDict = self._set_API_dict(
            kwargs.get("APIList", list())
        )

    def _set_API_dict(self, api_list):
        api_dict = dict(
            availible = list(),
            deplete = list()
        )
        for api in api_list:
            api_dict["availible"].append(api)

        return api_dict

    def _switch_API_key(self):
        print("switching DART API KEY")
        if self.APIDict.get("availible"):
            self.APIDict.get("availible").remove(self.APIKey)
            self.APIDict.get("deplete").append(self.APIKey)
            self.APIKey = self.APIDict.get("availible")[0]
        else:
            raise RuntimeError("No Availble APIKEY Left for OpenDart")

    def read(self, url = None, **params):
        ret, r = self.get(
            content_type=self.return_type(),
            **params
        )

        for condition in self.api_switch_event_conditions:
            while condition(r, content_type=self.return_type()):
                self._switch_API_key()
                ret, r = self.get(**params)

        return ret, r


class BaseOpenDartFileHandlerMixin(BaseFileHandlerMixin):
    """
    OpenDart offers zip file for report files and corporate codes.
    This Mixin gives a way for the API to dictify zip files.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        zf = zipfile.ZipFile(io.BytesIO(r.content))
        xml_data = zf.read('CORPCODE.xml')

    def open_zip_file(self, file, filename):
        with zipfile.ZipFile(io.BytesIO(file)) as myzip:
            zip_xml_dict = xmltodict.parse(myzip.read(filename))
            return zip_xml_dict

    def open_report_file(self, file):
        pass


class OpenDartPaginaterAPI(
        BaseOpenDartMultipleAPI,
        OpenDartAPIPaginatorMixin,
        ):

    pass


class OpenDartAPI(
        BaseOpenDartMultipleAPI,
        SingletonInstance,
        BaseOpenDartFileHandlerMixin,
        ):
    """
    Basically, we treat the opendart to return json data.
    However, certain endpoints such as cortp_code or business report only
    returns xml files and embedded in xml data.
    """
    pass