import json

import ArknightsDataParser
import ArknightsDataParser as ADP
from urllib.request import urlretrieve
import os
from PIL import Image, ImageTk


class Inventory:
    def __init__(self):
        self.inventory = {}
        for item in ADP.items["items"].values():
            if item["itemId"] == "4001" or item["itemId"] == "5001":
                self.inventory[item["itemId"]] = ADP.Item(item["itemId"])
            if item["classifyType"] == "MATERIAL" and item["itemType"] == "MATERIAL" and not item["obtainApproach"]:
                self.inventory[item["itemId"]] = ADP.Item(item["itemId"])
    None

