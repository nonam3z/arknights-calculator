from .files_loader import FileRepository
from .settings import Settings
from .singleton import Singleton


class Database(metaclass=Singleton):
    def __init__(self):
        self.rep = Settings().repository
        self.data = FileRepository(self.rep)
        self.ears = self.data.ears
        self.items = self.data.items
        self.formulas = self.data.formulas
        self.gameconst = self.data.gameconst
        self.materials = self.data.materials
        self.stages = self.data.stages
        self.zones = self.data.zones
        self.modules = self.data.modules
