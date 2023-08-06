# core.singleton_clas.py

class SingletonInstance():
  __instance = None

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

  @classmethod
  def __get_instance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__get_instance
    return cls.__instance