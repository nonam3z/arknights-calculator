import json


class Savedata:
    def __init__(self):
        self.savedata = json.load(open("savedata.json", encoding='utf-8'))