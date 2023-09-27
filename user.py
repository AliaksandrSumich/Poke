from database import DataBaseUsers

db = DataBaseUsers()


def get_all_users():
    users = {}
    users_dict = db.get_users_list()
    for user in users_dict.keys():
        users[int(user)] = User(user, name=users_dict[user]['name'], role=users_dict[user]['role'])
    return users




class User:
    def __init__(self, telegram_id, name=None, role=None):
        self.telegram_id = telegram_id

        if not name or not role:
            self.name, self.role = db.get_name_role(telegram_id)
        else:
            self.name, self.role = name, role

        self.semi_number = None
        self.stage_number = None
        self.question_number = None
        self.question = None
        self.answer_tag = None
        self.answer = None

    def set_question(self, semi_number, stage_number, question_number, question, answer_tag):
        self.semi_number = semi_number
        self.stage_number = stage_number
        self.question_number = question_number
        self.question = question
        self.answer_tag = answer_tag
        self.answer = None

    def reset_question(self, semi_number, stage_number):
        self.semi_number = semi_number
        self.stage_number = stage_number
        self.question_number = None
        self.question = None
        self.answer_tag = None
        self.answer = None


    def get_answer(self):
        """
        :return: answer = {
            'semi_number': self.semi_number,
            'stage_number': self.stage_number,
            'question_number': self.question_number,
            'question': self.question,
            'answer_tag': self.answer_tag,
            'answer': self.answer
        }
        """
        answer = {
            'semi_number': int(self.semi_number),
            'stage_number': self.stage_number,
            'question_number': self.question_number,
            'question': self.question,
            'answer_tag': self.answer_tag,
            'answer': self.answer
        }
        return answer


    def __str__(self):
        return f"""        
        telegram_id: {self.telegram_id}
        name: {self.name}
        role: {self.role}
        question_number: {self.question_number}
        question: {self.question}
        answer_tag: {self.answer_tag}        
        """
