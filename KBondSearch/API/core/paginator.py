import requests

from abc import abstractmethod

class BasePaginatorMixin():
    """
    A mixin class which calls the base class's read method to retreive data.
    This allows a easy retreiver classes to become iterators of data
    """

    def __init__(self, *args, **kwargs):
        self._set_paginator_params(r=None)

    def __str__(self):
        return str(self.__dict__)

    def __iter__(self, **params):
        self._first = True
        return self

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
            
        self._set_paginator_params(r)
        self._set_paginator_params_for_next()

        if self.cur_page_num < self.total_pages:
            return ret, r
        else:
            raise StopIteration

    @abstractmethod
    def _set_paginator_params_for_next(self, *args, **kwargs):
        pass

    @abstractmethod
    def _set_paginator_params(self, *args, **kwargs):
        pass

    @property
    def total_pages(self):
        return int(ceil(float(self.total) / self.per_page))