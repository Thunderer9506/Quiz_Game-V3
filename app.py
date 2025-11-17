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

@app.context_processor
def inject_global_vars():
    return dict(categories = CATEGORY)

@app.route("/",methods=['GET','POST'])
def home():
    global QUESTION
    if request.method == 'POST':
        category = request.form.get('category')
        type = request.form.get('type')
        difficulty = request.form.get('difficulty')
        QUESTION = getQuestion(category,difficulty,type)
        return redirect(url_for('quiz',questionId = 1))
        
    return render_template("index.html")

@app.route("/questionPage/<int:questionId>",methods=['GET','POST'])
def quiz(questionId):
    questions = QUESTION[questionId-1]
    print(questions)
    if request.method == 'POST':
        answer = request.form.get('answer')
        print(answer)
        return redirect(url_for('quiz',questionId = questionId + 1))
    return render_template("quiz.html",questions = questions)

if __name__ == "__main__":
    app.run(debug=True)