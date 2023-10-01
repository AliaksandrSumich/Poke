from datetime import datetime

from database import DataBaseSemi, DataBaseStat
from utils import find_tag, multiple_ingredients

semi_base = DataBaseSemi()
stat_base = DataBaseStat()


class Semi:
    def __init__(self, user, semi_name, semi_number):
        self.semi_number = semi_number
        self.user = user
        self.semi_name = semi_name
        self.stages = self.get_stages()
        self.current_stage = 0
        self.answers = []
        self.start_time = datetime.now()
        self.finish_time = None

    def get_stages(self):
        data = semi_base.get_data(self.semi_name)
        print('Headers', data[0])
        stages = []
        for stage in data[1:]:
            print(stage)
            stage_dict = {}
            for i, head in enumerate(data[0]):
                if i < len(stage):
                    stage_dict[head] = stage[i]
            stages.append(stage_dict)
        return stages

    def move_next_stage(self):
        self.current_stage += 1
        if self.current_stage < len(self.stages):
            return self.get_actual_stage()
        else:
            return None

    def get_actual_stage(self):

        stage = self.stages[self.current_stage]
        stage['semi_name'] = self.semi_name
        stage['semi_number'] = self.semi_number
        stage['stage_number'] = self.current_stage

        portions = find_tag(self.answers, '#количество порций')

        if portions:

            for key in stage.keys():
                stage[key] = multiple_ingredients(stage[key], portions)

        print(f'stage in get_actual_stage {stage}')

        return stage

    def set_answer(self, answer):
        if answer['answer']:
            answer['stage'] = self.current_stage

            self.answers.append(answer)
        else:
            print('bad answer')

    def get_current_stage_questions(self):
        stage = self.stages[self.current_stage]
        questions = []
        for key in stage.keys():
            if 'Вопрос' in key:
                question_number = key.split()[1]
                question_tag = stage.get(f'Хэштег {question_number}')
                if not question_tag:
                    continue
                question = {
                    'semi_number': self.semi_number,
                    'stage_number': self.current_stage,
                    'number': len(questions) + 1,
                    'question': stage[key],
                    'tag': question_tag
                }
                questions.append(question)
        return questions


    def next_question(self):

        answers = self.answers
        print('answers in next_question', answers)
        questions = self.get_current_stage_questions()

        print('questions in semi next_question', questions)
        if not questions:
            return None
        last_question_answered = -1
        for answer in answers:
            if answer['stage'] == self.current_stage:
                if answer['question_number'] > last_question_answered:
                    last_question_answered = answer['question_number']

        print(f'last_question_answered = {last_question_answered}')

        next_question_number = last_question_answered + 1

        if last_question_answered == -1:
            next_question_number = 1

        for question in questions:
            if question['number'] == next_question_number:
                return question

        return None

    def get_list_to_save(self):
        """
        Дата	ID заготовки	Телеграм ID сотрудника	Сотрудник	Заготовка	Время производства	Выход	Показатель эффективности	Стоимость производства

        """
        exit = find_tag(self.answers, '#вес готового продукта')
        start = find_tag(self.answers, '#вес сырого продукта')
        if exit and start:
            try:
                effect = 1 - (float(start)-float(exit))/float(start)
            except:
                print(f'wrong data format exit: {exit}, start {start}')
                effect = 'to do'  # f'wrong data format exit: {exit}, start {start}'
        else:
            effect = f'wrong data format exit: {exit}, start {start}'


        return [
            str(datetime.date(datetime.now())),
            self.semi_number,
            self.user.telegram_id,
            self.user.name,
            self.semi_name,
            str(datetime.now() - self.start_time),
            exit,
            effect,
            'to do'
        ]



    def __str__(self):

        return f"""
self.semi_number = {self.semi_number}
self.user = {self.user}
self.semi_name = {self.semi_name}
self.stages = {self.stages}
self.current_stage = {self.current_stage}
self.answers = {self.answers}
"""

class Kitchen:
    def __init__(self):
        self.semies = {}
        self.dishes = {}
        self.next_semi_number = stat_base.get_next_semi_number()


    def start_new_semi(self, user, semi_name):
        semi_number = self.next_semi_number
        self.next_semi_number += 1
        semi = Semi(user, semi_name, semi_number=semi_number)
        self.semies[semi_number] = semi

        return self.semies[semi_number].get_actual_stage()

    def finish_semi(self, semi_number):
        print(f'finishing semi {semi_number}')
        print(f'all semies {self.semies}')
        semi_number = int(semi_number)
        semi = self.semies[semi_number]
        semi.finish_time = datetime.now()
        stat_base.save_semi(semi)




    def move_next_stage(self, semi_number):

        return self.semies[int(semi_number)].move_next_stage()


    def set_semi_answer(self, answer):
        """
        answer = {
            'semi_number': self.semi_number,
            'question_number': self.question_number,
            'question': self.question,
            'answer_tag': self.answer_tag,
            'answer': self.answer
        }
        """

        self.semies[answer['semi_number']].set_answer(answer)
        print(self.semies[answer['semi_number']])
        return self.semies[answer['semi_number']].next_question()




if __name__ == '__main__':

    semi = Semi(123, 'Огурцы', 2)
    print(semi.get_actual_stage())
    print(semi)
    print(semi.get_current_stage_questions())


