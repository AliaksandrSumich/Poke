from database import DataBaseUsers

db = DataBaseUsers()

class User:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id
        self.name, self.role = db.get_name_role(telegram_id)

