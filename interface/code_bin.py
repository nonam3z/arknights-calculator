

@staticmethod
def save_settings():
    settings_obj = ADP.Settings()
    if os.path.exists("../settings.json"):
        os.remove("../settings.json")
    file = open("../settings.json", 'w+')
    json.dump(settings_obj, file, cls=EarEncoder, indent=4)
    file.close()


def load_settings(self):
    if os.path.exists("../settings.json"):
        size = os.path.getsize("../settings.json")
        if size:
            settings = json.load(open("../settings.json", encoding='utf-8'))
        else:
            settings = {}
    else:
        settings = {"repository": "en_US"}
    if settings:
        if settings.get("repository"):
            self.settings.repository = settings.get("repository")
            self.rep_choose_var.set(self.settings.repository)
        else:
            self.rep_choose_var.set("en_US")
