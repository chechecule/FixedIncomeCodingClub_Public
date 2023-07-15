# OpenDart/paginators.py
import xmltodict

from core.paginator import BasePaginatorMixin


class FSCAPIPaginatorMixin(BasePaginatorMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_paginator_params(
            self, **kwargs
        ):
        self._iterator_params = {
            "pageNo" : str(kwargs.get("pageNo", 1)),
            "numOfRows" : str(kwargs.get("numOfRows", 100)),
        }

    def _set_paginator_params_from_ret(
            self, r
        ):
        """
        set pagination parameters from the returend page. 
        this private method ensures that his paginator doesn't break from
        cases which the API does not properly reflect request parameters
        """

        xml_return = xmltodict.parse(r.content)
        self._iterator_params["pageNo"] = xml_return["pageNo"]
        self._iterator_params["numOfRows"] = xml_return["numOfRows"]

        self._total_page = round(xml_return["totalCount"]/xml_return[totalCount"numOfRows"])

    def _set_paginator_params_for_next(self):
        self._iterator_params["pageNo"] += 1

    def initialize_params_for_iterator(self, **params):
        self.non_iterator_params = params

    def __next__(self, **params):
        """
        Overwrite this if there is no page!
        """
        params.update(self.non_iterator_params)

        if self._first:
            ret, r = self.read(**params)
            self._first = False
        else:
            params.update(self._iterator_params)
            ret, r = self.read(**params)

        if ret:
            self._set_paginator_params_from_ret(r)

            if int(self._iterator_params["pageNo"]) < int(self._total_page):
                self._set_paginator_params_for_next()
                return ret, r
            else:
                raise StopIteration

        else:
            raise StopIteration
