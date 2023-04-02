


def check_error_typing(self):
    checkBox = messagebox.askquestion(title="Clearing Inventory", message="Are you sure? "
                                                                          "This will remove all data from inventory "
                                                                          "tab! \nThis action cannot be undone.")
    if checkBox == "yes":
        self.inventory.clear_inventory()
    return None


def change_repository(self):
    if self.rep_choose_var.get() in ["en_US", "zh_CN", "ja_JP", "ko_KR", "zh_TW"]:
        self.save_data()
        self.update_data()
        self.calculator.clear_all()
        self.farming.clear_all()
        self.crafting.clear_all()
        self.itemData.clear_all()
        self.load_data()
        self.itemData.create_info()
    else:
        self.rep_choose_var.set(self.settings.repository)


def update_data(self):
    self.inventory.clear_inventory()
    if os.path.exists("jsons/" + self.rep_choose_var.get()):
        ADP.LoadFiles(self.rep_choose_var.get(), False).run()
    else:
        ADP.LoadFiles(self.rep_choose_var.get(), True).run()
    self.update_variables()
    self.planner.selectOperator["values"] = ADP.return_list_of_ears()
    self.inventory.update_inventory()
    self.calculator.create_item_list()
    self.farming.create_item_list()
    self.settings.repository = self.rep_choose_var.get()





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


def load_data(self):
    if os.path.exists("jsons/" + self.settings.repository + "/savedata.json"):
        size = os.path.getsize("jsons/" + self.settings.repository + "/savedata.json")
        if size:
            self.update_variables()
            savedata = json.load(open("jsons/" + self.settings.repository + "/savedata.json", encoding='utf-8'))
            self.planner.del_all_ears()
            try:
                for ear in savedata["earList"].values():
                    name = ear["name"]
                    iid = ear["iid"]
                    sc = ear["current"]
                    sd = ear["desired"]
                    current = ADP.Stats(sc["elite"], sc["level"], sc["skill1"], sc["skill2"],
                                        sc["skill3"])
                    desired = ADP.Stats(sd["elite"], sd["level"], sd["skill1"], sd["skill2"],
                                        sd["skill3"])
                    operator = ADP.OperatorState(iid, name, current, desired)
                    self.planner.allEarsList.setdefault(operator.name)
                    self.planner.allEarsList[operator.name] = operator
                    self.planner.earsList.insert("", tk.END,
                                                 values=(
                                                     name, self.planner.create_upgrade_string(current, desired)),
                                                 iid=iid)
            except KeyError:
                print("KeyError in savedata.json --> earList.")
            try:
                for item in savedata["inventory"].values():
                    iFrame.InventoryFrame.frames[item["itemId"]].itemHave.set(int(item["have"]))
            except KeyError:
                print("KeyError in savedata.json --> inventory.")
            try:
                self.stages.clear_all()
                self.stages.create_visible_tree(savedata["stages"]["checked_list"])
            except KeyError:
                self.stages.clear_all()
                self.stages.create_visible_tree({})
                print("KeyError in savedata.json --> stages.")
    else:
        return None


def update_variables(self):
    settings_obj = ADP.Settings()
    settings_obj.repository = self.rep_choose_var.get()
    self.save_settings()
    ADP.Database.clear()
    ADP.Database()
    ADP.Inventory.clear()
    ADP.Inventory()


def update_tabs_data(self, event):
    self.planner.create_results_list("")
    self.update()


class EarEncoder(json.JSONEncoder):
    def default(self, obj):
        instances = (ADP.OperatorState, ADP.Stats, ADP.Settings, iFrame.InventoryFrame, ADP.Operator, ADP.Item, ADP.Inventory)
        if isinstance(obj, instances):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

