# core/wrapper_decorators.py

from .singleton_class import SingletonInstance

class WrapperMissingKwargsError(Exception):
    """Raised when wrapper function did not receive enough kwargs"""
    def __init__(self, missing_keys):
        self._message = f"Wrapper missing {missing_keys} kwargs"
        super().__init__(self._message)

class WrapperRecommendedKwargsComplainerClass(SingletonInstance):

    def __init__(self, missing_keys):
        self.complained_functions = list()
        self.missing_keys = missing_keys

    def complain(self, func):
        if func.__name__ in self.complained_functions:
            pass
        else:
            print(f"Wrapper missing {missing_keys} kwargs. Those are recommended")
            self.complained_functions.append(func.__name__)


def required_kwargs(required_key_list):
    def wrapper(func):
        def decorator(*args, **kwargs):
            for key, value in kwargs.items():
                if key in required_key_list: required_key_list.remove(key)
            if required_key_list:
                raise WrapperMissingKwargsError(required_key_list)

            return func(*args, **kwargs)
        return decorator

    return wrapper

def recommended_kwargs(recommended_key_list):
    def wrapper(func):
        def decorator(*args, **kwargs):
            for key, value in kwargs.items():
                if key in recommended_key_list: recommended_key_list.remove(key)
            if recommended_key_list:
                sWrapperRecommendedKwargsComplainerClass(True, recommended_key_list).complain(func)

            return func(*args, **kwargs)
        return decorator

    return wrapper