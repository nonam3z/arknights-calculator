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
        if os.path.exists(f"jsons/{rep}"):
            date_file = datetime.datetime.fromtimestamp(os.path.getmtime(f"jsons/{rep}"))
        else:
            date_file = datetime.datetime.now()
        # print(f"{date_github} // git -- file // {date_file} // rep: {rep} // filename: {filename}")
        bool_check = date_github > date_file
        # print(f"Check git > file: {bool_check}")
        if bool_check or (force is True):
            os.makedirs("../jsons", exist_ok=True)
            if filename == "materials.json":
                self.get_penguin_matrix(rep)
            else:
                self.get_file(filename, rep)

    @staticmethod
    def check_github(rep: str):
        try:
            g = github.Github()
            repo = g.get_repo("Kengxxiao/ArknightsGameData_YoStar")
            commits = repo.get_commits(path=f"{rep}/gamedata")
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
        repository = f"https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/master/{rep}/gamedata/excel/"
        url = f"{repository}{filename}"
        os.makedirs(f"jsons/{rep}/", exist_ok=True)
        file = f"jsons/{rep}/{filename}"
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
        file = f"jsons/{rep}/materials.json"
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
        url = f"{repository}{filename}.png"
        os.makedirs("../items/", exist_ok=True)
        file = f"items/{filename}.png"
        if os.path.exists(file):
            if os.path.getsize(file) == 0:
                os.remove(file)
        if not os.path.exists(file):
            data = requests.get(url=url).content
            if data.__len__() > 20:
                open(file, 'wb+').write(data)


class FileRepository:
    def __init__(self, rep: str, force: bool):

        params = { "ears": "character_table.json",
                   "items": "item_table.json",
                   "formulas": "building_data.json",
                   "gameconst": "gamedata_const.json",
                   "materials": "materials.json",
                   "stages": "stage_table.json",
                   "zones": "zone_table.json",
                   "modules": "uniequip_table.json" }

        def load_files():
            for key, filename in params.items():
                setattr(self, key, json.load(open(f"jsons/{rep}/{filename}", encoding='utf-8')))

        try:
            if not force:
                load_files()
            if force:
                for file in params.values():
                    LoadFiles(file, rep, True)
                load_files()
        except json.JSONDecodeError as error:
            print(error.doc)
            for file_name in os.listdir(f"jsons/{rep}"):
                if os.path.isfile(f"jsons/{rep}/{file_name}"):
                    os.remove(f"jsons/{rep}/{file_name}")
            LoadFiles(error.doc, rep, True)
        except FileNotFoundError as error:
            print(error.filename)
            print("Database is corrupted or missing, redownloading...")
            LoadFiles(error.filename, rep, True)