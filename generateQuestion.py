import requests
import random
import html

def getQuestion(category:str ="any", difficulty:str="any", type:str="any") -> list:
    api_link = "https://opentdb.com/api.php?amount=10"
    params = ""
    if category != 'any':
        params += "&category=" + category
    if difficulty != 'any':
        params += "&difficulty=" + difficulty
    if type != 'any':
        params += "&type=" + type
    
    api_link += params
    results = requests.get(api_link).json()
    questions = []

    id = 1
    for i in results['results']:
        options = [html.unescape(opt) for opt in i['incorrect_answers']]
        options.append(html.unescape(i['correct_answer']))
        random.shuffle(options)

        questions.append({
            "id": id,
            "question": html.unescape(i['question']),
            "options": options,
            "correct": html.unescape(i['correct_answer']),
            "category": i['category']
        })
        id += 1

    return questions
