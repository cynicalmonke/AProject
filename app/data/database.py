import json

class Database:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "AppConfig": {},
                "UserData": {
                    "logged-in": False
                },
                "Collections": {},
                "Assets": {}
            }

    def save(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def add_button(self, button_name, button_data):
        self.data["Collections"][button_name] = button_data
        self.save()

    def remove_button(self, button_name):
        if button_name in self.data["Collections"]:
            del self.data["Collections"][button_name]
            self.save()
        else:
            print(f"Button '{button_name}' not found in Collections.")