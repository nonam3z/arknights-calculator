import re

from .database import Database


def create_stages_tree():
    stages_db = Database().stages
    zones_db = Database().zones
    zones = {}
    for stage in stages_db.values():
        if not zones.get(stage["zoneId"]):
            zones.setdefault(stage["zoneId"], {})
    pattern = r"(main).*|(weekly).*"
    zones2 = zones.copy()
    for zone in zones2:
        if not re.fullmatch(pattern, zone):
            zones.pop(zone)
    for stage in stages_db.values():
        if stage["zoneId"] in zones:
            if not zones[stage["zoneId"]].get(stage["stageId"]):
                stagespattern = r".*(#f#)|(tr).*"
                if not re.fullmatch(stagespattern, stage["stageId"]):
                    zones[stage["zoneId"]].setdefault(stage["stageId"], stage)
    for zone in zones:
        if zones_db[zone].get("zoneNameFirst"):
            zones[zone]["name"] = zones_db[zone].get("zoneNameFirst")
        else:
            zones[zone]["name"] = zones_db[zone].get("zoneNameSecond")
    return zones