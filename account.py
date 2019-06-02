import json, random

class account(object):
    def __init__(self, FILENAME = "account"):
        try:
            file = open(FILENAME+".txt", "r")
            info = json.loads(file.read())
            file.close()
        except:
            info = self.create_account()
            self.set_account_info(info)
        self.ID = info["ID"]
        self.name = info["name"]
        self.password = info["password"]
        self.level = info["level"]
        self.exp = info["exp"]

    def create_account(self):
        name = raw_input("Create new account.\n name: ")
        info = {"ID": int(random.random()*1000),
                "name": name,
                "password": "1234",
                "level": 1,
                "exp": 0}
        return info

    def update_name(self, NAME):
        self.name = NAME

    def update_password(self, PASSWORD):
        self.password = PASSWORD

    def update_exp(self, AMOUNT):
        self.exp += AMOUNT
        if self.exp >= 100:
            self.level += 1
            self.exp -= 100

    def save_account_info(self, FILENAME = "account"):
        f_account = open(FILENAME+".txt", "w")
        f_account.write(json.dumps(INFO, indent = 4, sort_keys = True))
        f_account.close()
        return True

