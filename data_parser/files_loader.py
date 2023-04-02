# Arknights Operators Promotion Calculator
# Copyright (C) 2021 NoNaM3z
# email: anton.gf.feo@gmail.com

import datetime
import json
import os
import threading

import github
import requests


class LoadFiles(threading.Thread):
    def __init__(self, filename: str, rep: str, force: bool):
        """
        Создание/обновление базы данных для работы программы.
        :param filename: Имя скачиваемого файла.
        :param rep: Текущий выбранный репозиторий.
        :param force: Флаг проверки принудительного обновления базы.
        """
        super().__init__()

        date_github = self.check_github(rep)
        if os.path.exists("jsons/" + rep):
            date_file = datetime.datetime.fromtimestamp(os.path.getmtime(("jsons/" + rep)))
        else:
            date_file = datetime.datetime.now()
        print(str(date_github) + " // git -- file // " + str(date_file) + " // rep: " + rep)
        bool_check = date_github > date_file
        print("Check git > file: " + str(bool_check))
        if bool_check or (force is True):
            os.makedirs("../jsons", exist_ok=True)
            if filename == "materials":
                self.get_penguin_matrix(rep)
            else:
                self.get_file(filename, rep)

    @staticmethod
    def check_github(rep: str):
        try:
            g = github.Github()
            repo = g.get_repo("Aceship/AN-EN-Tags")
            commits = repo.get_commits(path=("json/gamedata/" + rep + "/gamedata"))
            date = commits[0].commit.committer.date
        except github.GithubException:
            date = datetime.datetime.fromtimestamp(0)
        return date

    @staticmethod
    def get_file(filename: str, rep: str):
        """
        Метод для получения файлов из репозитория github.
        :param rep: Принимает на вход текущий выбранный репозиторий.
        :param filename: Принимает на вход имя файла.
        """
        repository = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/" + str(rep)\
                     + "/gamedata/excel/"
        url = (repository + filename + ".json")
        os.makedirs(("jsons/" + rep + "/"), exist_ok=True)
        file = ("jsons/" + rep + "/" + filename + ".json")
        if os.path.exists(file):
            os.remove(file)
        data = requests.get(url=url).json()
        open(file, 'w+').write(json.dumps(data))

    @staticmethod
    def get_penguin_matrix(rep: str):
        """
        Метод для получения матрицы стоимости и частоты выпадения материалов с Penguin Statistics.
        :param rep: Принимает на вход текущий выбранный репозиторий.
        """
        repository = "https://penguin-stats.io/PenguinStats/api/v2/result/matrix"
        file = "jsons/" + rep + "/materials.json"
        reps = ["en_US", "zh_CN", "ja_JP", "ko_KR", "zh_TW"]
        servers = ["US", "CN", "JP", "KR", "CN"]
        if rep in reps:
            server = servers[reps.index(rep)]
        else:
            server = "US"
        if os.path.exists(file):
            os.remove(file)
        PARAMS = {"server": server, "show_closed_zones": False}
        data = str(requests.get(url=repository, params=PARAMS).content)
        data = data[2:-1:]
        open(file, 'w+').write(data)


class LoadImages(threading.Thread):
    def __init__(self, filename: str):
        super().__init__()

        repository = "https://raw.githubusercontent.com/Aceship/Arknight-Images/main/items/"
        url = (repository + filename + ".png")
        os.makedirs("../items/", exist_ok=True)
        file = ("items/" + filename + ".png")
        if os.path.exists(file):
            if os.path.getsize(file) == 0:
                os.remove(file)
        if not os.path.exists(file):
            data = requests.get(url=url).content
            if data.__len__() > 20:
                open(file, 'wb+').write(data)


class FileRepository:
    def __init__(self, rep: str):
        try:
            self.ears = json.load(open("jsons/" + rep + "/character_table.json", encoding='utf-8'))
            self.items = json.load(open("jsons/" + rep + "/item_table.json", encoding='utf-8'))
            self.formulas = json.load(open("jsons/" + rep + "/building_data.json", encoding='utf-8'))
            self.gameconst = json.load(open("jsons/" + rep + "/gamedata_const.json", encoding='utf-8'))
            self.materials = json.load(open("jsons/" + rep + "/materials.json", encoding='utf-8'))["matrix"]
            self.stages = json.load(open("jsons/" + rep + "/stage_table.json", encoding='utf-8'))["stages"]
            self.zones = json.load(open("jsons/" + rep + "/zone_table.json", encoding='utf-8'))["zones"]
            self.modules = json.load(open("jsons/" + rep + "/uniequip_table.json", encoding='utf-8'))
        except json.JSONDecodeError as error:
            print(error.doc)
            for file_name in os.listdir("jsons/" + rep):
                if os.path.isfile("jsons/" + rep + "/" + file_name):
                    os.remove("jsons/" + rep + "/" + file_name)
            LoadFiles(error.doc, rep, True)
        except FileNotFoundError as error:
            print(error.filename)
            print("Database is corrupted or missing, redownloading...")
            LoadFiles(error.filename, rep, True)

# print("Getting characters data...")
# self.get_file("character_table", rep)
# print("Getting items data...")
# self.get_file("item_table", rep)
# print("Getting formulas data...")
# self.get_file("building_data", rep)
# print("Getting game constants...")
# self.get_file("gamedata_const", rep)
# print("Getting module data...")
# self.get_file("uniequip_table", rep)
# print("Getting zones data...")
# self.get_file("zone_table", rep)
# print("Getting stages data...")
# self.get_file("stage_table", rep)
