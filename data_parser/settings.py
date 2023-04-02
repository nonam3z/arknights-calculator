from .singleton import Singleton


class Settings(metaclass=Singleton):
    def __init__(self):
        self.repository = "en_US"
