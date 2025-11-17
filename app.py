from flask import Flask,render_template,request,redirect,url_for,session
from generateQuestion import getQuestion
import secrets

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
app.secret_key = secrets.token_urlsafe(32)


@app.context_processor
def inject_global_vars():
    return dict(categories = CATEGORY)

@app.route("/",methods=['GET','POST'])
def home():
    session.clear()

    if request.method == 'POST':
        category = request.form.get('category')
        type_ = request.form.get('type')
        difficulty = request.form.get('difficulty')

        session['questions'] = getQuestion(category,difficulty,type_)
        session['score'] = 0

        return redirect(url_for('quiz',questionId = 1))
        
    return render_template("index.html")

@app.route("/questionPage/<int:questionId>",methods=['GET','POST'])
def quiz(questionId):
    # What if the user bookmarked this page, questions wont be present
    # in session giving us errors
    if 'questions' not in session or not session['questions']:
        return redirect(url_for('home'))
    
    all_questions = session.get('questions',[])
    
    if questionId >= len(all_questions):
        return redirect(url_for('score'))
    
    current_questions = all_questions[questionId-1]

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer:
            choosen_option_text = current_questions['options'][int(answer)-1]
            if current_questions['correct'] == choosen_option_text:
                session['score'] = session.get('score',0)+1

        return redirect(url_for('quiz',questionId = questionId + 1))
    return render_template("quiz.html",questions = current_questions,total_questions = len(all_questions))

@app.route("/score")
def score():
    return render_template("score.html",score = session.get('score'),
                                        total = len(session.get('questions',[])))

if __name__ == "__main__":
    app.run(debug=False)