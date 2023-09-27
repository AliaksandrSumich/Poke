def find_tag(answers, tag):
    """
    [{'semi_number': 1, 'stage_number': 0, 'question_number': 1, 'question': 'введите вес огурцов', 'answer_tag': '#вес сырого продукта', 'answer': '3000', 'stage': 0},
    {'semi_number': 1, 'stage_number': 2, 'question_number': 1, 'question': 'Введите количество упаковок', 'answer_tag': '#количество упаковок', 'answer': '5', 'stage': 2},
    {'semi_number': 1, 'stage_number': 2, 'question_number': 2, 'question': 'Введите общий вес упаковок', 'answer_tag': '#вес готового продукта', 'answer': '2800', 'stage': 2}]

    """
    for answer in answers:
        if answer.get('answer_tag'):
            if answer['answer_tag'] == tag:
                return answer['answer']
    return None
