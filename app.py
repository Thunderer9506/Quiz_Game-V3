from flask import Flask,render_template,request,redirect,url_for
from generateQuestion import getQuestion

CATEGORY = ["General Knowledge","Entertainment: Books",
            "Entertainment: Film","Entertainment: Music",
            "Entertainment: Musicals & Theatres","Entertainment: Television",
            "Entertainment: Video Games","Entertainment: Board Games",
            "Science & Nature","Science: Computers","Science: Mathematics",
            "Mythology","Sports","Geography","History","Politics","Art",
            "Celebrities","Animal","Vehicles","Entertainment: Comics",
            "Science: Gadgets","Entertainment: Japenese Anime & Manga",
            "Entertainment: Cartoon & Animation"]


app = Flask(__name__)

QUESTION = None
SCORE = 0

@app.context_processor
def inject_global_vars():
    return dict(categories = CATEGORY)

@app.route("/",methods=['GET','POST'])
def home():
    global QUESTION, SCORE
    SCORE = 0
    if request.method == 'POST':
        category = request.form.get('category')
        type = request.form.get('type')
        difficulty = request.form.get('difficulty')
        QUESTION = getQuestion(category,difficulty,type)
        return redirect(url_for('quiz',questionId = 1))
        
    return render_template("index.html")

@app.route("/questionPage/<int:questionId>",methods=['GET','POST'])
def quiz(questionId):
    global SCORE
    if questionId >= 10:
        return redirect(url_for('score'))
    questions = QUESTION[questionId-1]
    print(questions)
    if request.method == 'POST':
        answer = request.form.get('answer')
        print(answer)
        if questions['correct'] == questions['options'][int(answer)-1]:
            SCORE += 1
        return redirect(url_for('quiz',questionId = questionId + 1))
    return render_template("quiz.html",questions = questions)

@app.route("/score")
def score():
    return render_template("score.html",result = {'score':SCORE,'total':10})

if __name__ == "__main__":
    app.run(debug=True)