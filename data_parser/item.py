import math


class Item:
    def __init__(self, itemid, name, iconid, rarity):
        self.itemId = itemid
        self.name = name
        self.iconId = iconid
        self.iconSmall = None
        self.iconMedium = None
        self.iconLarge = None
        self.rarity = rarity
        self.itemCraftingId = None
        self.formula = []
        self.stages = None
        self.bestAp = math.inf
        self.craftingAp = 0
        self.bestStage = ""
        self.bestStageId = ""
        self.flags = ""
