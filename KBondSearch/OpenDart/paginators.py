# OpenDart/paginators.py
import json

from core.paginator import BasePaginatorMixin


class OpenDartAPIPaginatorMixin(BasePaginatorMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_paginator_params(
            self, **kwargs
        ):
        self._iterator_params = {
            "page_no" : str(kwargs.get("page_no", 1)),
            "page_count" : str(kwargs.get("page_count", 100)),
            "sort_mth" : kwargs.get("sort_mth", "desc"),
            "sort" : kwargs.get("sort", "date")
        }

    def _set_paginator_params_from_ret(
            self, r
        ):
        """
        set pagination parameters from the returend page. 
        this private method ensures that his paginator doesn't break from
        cases which the API does not properly reflect request parameters
        """

        json_return = json.loads(r.content)
        self._iterator_params["page_count"] = json_return["page_count"]
        self._iterator_params["page_no"] = json_return["page_no"]

        self._total_page = json_return["total_page"]

    def _set_paginator_params_for_next(self):
        self._iterator_params["page_no"] += 1

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

            if int(self._iterator_params["page_no"]) < int(self._total_page):
                self._set_paginator_params_for_next()
                return ret, r.json()
            else:
                raise StopIteration

        else:
            raise StopIteration
