import pygsheets as pygsheets

class DataBaseSemi:
    id_sp = '1ZpqjJ_KFlKVDft_O69go--q7vuYlJa5Mj6dxRO407Bs'

    def __init__(self):
        self.sh = self.get_table_object()

    def get_table_object(self):
        gc = pygsheets.authorize(service_account_file='shurick-programist-67d09e08c45d.json')
        gc.create('my_shiit')
        sh = gc.open_by_key(DataBaseSemi.id_sp)
        return sh

    def semi_list(self):
        sheets = self.sh.worksheets()
        names = []
        for sheet in sheets:
            names.append(sheet.title)
        return names

    def get_data(self, semi_name):

        try:
            worksheet = self.sh.worksheet('title', semi_name)
            data = worksheet.get_all_values(include_tailing_empty=False,
                                              include_tailing_empty_rows=False)
            return data
        except:
            return []


class DataBaseUsers:
    id_sp = '1v0G08fDEfybzI5t0EkX4tdCGfc0B2Q8xtC6_zFCpjvo'

    def __init__(self):
        self.sh = self.get_table_object()
        self.users_worksheet = self.sh.worksheet('title', 'Users')

    def get_table_object(self):
        gc = pygsheets.authorize(service_account_file='shurick-programist-67d09e08c45d.json')
        gc.create('my_shiit')
        sh = gc.open_by_key(DataBaseUsers.id_sp)
        return sh

    def get_data(self):

        try:
            data = self.users_worksheet.get_all_values(include_tailing_empty=False,
                                              include_tailing_empty_rows=False)
            return data
        except:
            return []

    def get_users_list(self):
        """
        :return: {'1223': {'name': 'Alex', 'role': 'worker'}, '1227721841': {'name': 'Aliaksandr', 'role': 'user'}}
        """
        data = self.get_data()
        print(data)
        keys = data[0][1:]
        print(keys)
        users = {}

        for user in data[1:]:
            temp_dict = {}
            for i, key in enumerate(keys):
                temp_dict[key] = user[i + 1]

            users[user[0]] = temp_dict
        return users

    def get_name_role(self, telegram_id):
        users = self.get_users_list()

        return (users[telegram_id]['name'], users[telegram_id]['role'])

    def write_new_user(self, user):
        """
        ['telegram_id', 'name', 'role']
        """
        users = self.get_users_list()
        print('users', users)
        print(user[0], users)

        if str(user[0]) not in users:
            self.users_worksheet.append_table(user, start=None, end=None, dimension='ROWS', overwrite=False)

class DataBaseStat:
    id_sp = '1WGqedvSgZRhUNc2RW6kmEiXTGdzrQhTz4HHm9LTmgCo'

    def __init__(self):
        self.sh = self.get_table_object()
        self.stat_worksheet = self.sh.worksheet('title', 'Заготовки')

    def get_table_object(self):
        gc = pygsheets.authorize(service_account_file='shurick-programist-67d09e08c45d.json')
        gc.create('my_shiit')
        sh = gc.open_by_key(DataBaseStat.id_sp)
        return sh

    def get_next_semi_number(self):
        numbers = self.stat_worksheet.get_col(2,  include_tailing_empty=False)[1:]
        print(f'numbers from database {numbers}')
        if numbers:

            numbers = [int(x) for x in numbers]

            print()
            return int(max(numbers)) + 1
        else:
            return 0

    def save_semi(self, semi):
        list_to_save = semi.get_list_to_save()
        print(f'list_to_save {list_to_save}')
        try:
            self.stat_worksheet.append_table(list_to_save, start=None, end=None, dimension='ROWS', overwrite=False)
        except Exception as e:
            print(f'Exception in save_semi {e}')



if __name__ == '__main__':
    # db = DataBaseUsers()
    # db.write_new_user(['1223', 'Alex', 'worker'])
    # print(db.get_users_list())

    # db = DataBaseSemi()
    # # print(db.semi_list())
    # print(db.get_data('Огурцы'))

    db = DataBaseStat()
    print(db.get_next_semi_number())