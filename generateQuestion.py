import requests


def getQuestion(category = None,difficulty=None, type= None):
    result = requests.get("https://opentdb.com/api.php?amount=10&category=11&difficulty=easy&type=multiple")
    params = ""
    if category:
        params += "&category="+category
    if difficulty:
        params += "&difficulty="+difficulty
    if type:
        params += "&type="+type