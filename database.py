import pygsheets as pygsheets

id_sp = '1ZpqjJ_KFlKVDft_O69go--q7vuYlJa5Mj6dxRO407Bs'

class DataBase:
    def __init__(self):
        self.sh = self.get_table_object()


    def get_table_object(self):
        gc = pygsheets.authorize(service_account_file='shurick-programist-67d09e08c45d.json')
        gc.create('my_shiit')
        sh = gc.open_by_key(id_sp)
        return sh


    def get_data(self):
        """
        Возвращает список из списков сумм сделок указанного филиала за указанную дату (формат даты: месяц.год)
        Список[0] - перечень ФИО
        Список[1] - перечень id
        Список[2..] - нулевой элемент - дата в формате "дата.месяц", остальные элементы - суммы сделок за указанную дату
        соответствующие id из списка[1]
        """


        # https://docs.google.com/spreadsheets/d/1-U_1HA8NUbIZuNie34P4Qjn-5mDNfawQ-5P8k-FzHNc/edit#gid=0



        try:
            worksheet = self.sh.worksheet('title', 'Огурцы')
            dannye = worksheet.get_all_values(include_tailing_empty=False,
                                              include_tailing_empty_rows=False)
            return dannye
        except:
            return []

if __name__=='__main__':
    db = DataBase()
    print(db.get_data())