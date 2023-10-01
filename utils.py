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




def multiple_ingredients(text, x):
    if text:
        text = str(text)
    else:
        return text
    if '{' not in text:
        return text
    parts = text.split('{')

    if x:
        x = float(x)
    else:
        return text

    res = ''
    for part in parts:
        if '}' not in part:
            res += part
            continue
        value = float(part.split('}')[0])
        res += f"{value * x}{part.split('}')[1]}"

    return res.replace(':', ':\n').replace(';', ';\n')




if __name__ == '__main__':
    pass
#     text = """Ингредиенты:
# соевый соус — {150} мл;
# молотый имбирь — {2} ч. ложки;
# жидкий мед — {1} ст. ложка;
# картофельный крахмал — {2} ч. ложки без горки;
# растительное масло (рафинированное) — {1} ч. ложка;
# сушеный чеснок — {1} ч. ложка;
# тростниковый сахар — {4}-{5} ч. ложек;
# вода — {60} мл;
# уксус винный 6% — {1} ст. ложка.
#     """
#     x = 10
#     print(multiple_ingredients(text, x))

