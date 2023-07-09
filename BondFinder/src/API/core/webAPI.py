import requests

from abc import abstractmethod

class BaseOpenAPI():
    """
    Base Open WebAPI class to be extended.
    This will allow easy setting up specific class cases of API modules.

    The class allows the specific use cases to set get or post methods as base retrieving
    http methods.

    The inheriting module will redefine the "read" and "url" method.

    Moreover, this validator checker function which automatically checks data for validation
    after retrieving data is supplied.
    """

    validators = []

    def __init__(self, APIKey, *args, **kwargs):
        self.APIKey = APIKey
        self.skip_validation = False
        self.headers = {"User-Agent" : "Mozilla/5.0"}

    @property
    @abstractmethod
    def url(self, **params):
        return NotImplementedError

    @abstractmethod
    def read(self, **params):
        """
        Set Get or Post
        """
        pass

    @abstractmethod
    def _add_params(self, **params):
        pass

    def _validate_response(self, resp, content_type = None, *args, **kwargs):
        if self.skip_validation:
            return True
        is_valid = True
        for validator in self.validators:
            is_valid = validator(resp, content_type, *args, **kwargs)
            if is_valid == False:
                return False
        return True

    def get(self, **params):
        params = self._add_params(**params)
        r = requests.get(self.url, headers=self.headers, params=params)
        if self._validate_response(r, params.get("content_type", None)):
            return True, r
        else:
            return False, r

    def post(self, **params):
        params = self._add_params(**params)
        r = requests.post(self.url + self.path, headers=self.headers, params=params)
        if self._validate_response(r, params.get("content_type", None)):
            return True, r
        else:
            return False, r