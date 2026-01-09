from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from agents.QuestionAgent import Agent as QuestionAgent
from agents.EvaluationAgent import Agent as EvaluationAgent
from flask_migrate import Migrate
from models import db
from schemas.user import User
from schemas.question import Question
from schemas.quiz_session import Sessions
from sqlalchemy.exc import IntegrityError
import markdown
import logging
import bleach
import uuid

# Create and configure logger
logging.basicConfig(filename="mainApp.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

load_dotenv()

class Config:
    def __init__(self):
        self.session = session

    def initSessions(self,questions):
        self.session["score"] = 0
        self.session["questions"] = questions.model_dump()
        self.session["performance_metrics"] = {"category": {}, "difficulty": {"easy": [], "medium": [], "hard": []}}
        self.session["user_answers"] = {}
    
    
    def update_score(self):
        current_score = self.session.get("score", 0)
        if isinstance(current_score, int):
            self.session["score"] = current_score + 1
        else:

            logger.warning(f"Invalid score type: {type(current_score)}")
    def get_score(self):
        return self.session.get("score",0)

    def total_questions(self):
        return len(self.session['questions']['questions'])

    def islastSessionactive(self):
        if self.total_questions() > len(self.session["user_answers"].keys()):
            return True
        return False
    
    def getQuestion(self,id:int):
        try:
            if 1 <= id <= self.total_questions():
                return self.session['questions']['questions'][id - 1]
            return False
        except Exception as e:
            logger.error(f"Error getting question {id}: {e}")
            return False
    def get_performance_metrics(self):
        return self.session.get('performance_metrics',{})

    def update_performance_metrics(self,category, difficulty, score):
        if category not in self.session["performance_metrics"]["category"]:
            self.session["performance_metrics"]["category"][category] = [score]
        else:
            self.session["performance_metrics"]["category"][category].append(score)

        self.session["performance_metrics"]["difficulty"][difficulty].append(score)


    def clear_session(self):
        self.session.clear()
    
    def insert_answer(self, question_key, current_questions, answer, q_type):
        user_answers = self.session.get("user_answers", {})
        user_answers[question_key] = {
            "question": current_questions["Question"],
            "user_answer": answer,
            "correct_answer": current_questions["Correct"],
            "type": q_type,
            "category": current_questions["Category"],
            "difficulty": current_questions["Difficulty"]
        }
        self.session["user_answers"] = user_answers



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/quiz_app"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

if os.getenv("SECRET_KEY"):
    app.secret_key = os.getenv("SECRET_KEY")

question_agent = QuestionAgent()
eval_agent = EvaluationAgent()
config = Config()


@app.route("/")
def index():
    return render_template("auth.html")

@app.post("/login")
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    is_exist = User.query.filter_by(email=email).first()
    if is_exist:
        if is_exist.password_hash == password:
            session["user_id"] = is_exist.id
            return redirect(url_for("home"))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    else:
        flash('Invalid username or password. Please try again.', 'error')
    return redirect(url_for("index"))

@app.post("/signup")
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    if password != confirm_password:
        flash('Passwords do not match. Please try again.', 'error')
        return redirect(url_for("index"))
    
    try:
        new_user = User(id=uuid.uuid4(),username=username,email=email,password_hash=password)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return redirect(url_for("home"))
    except IntegrityError as e:
        logger.error(f"User already excist {e}")
        flash('User already Excist', 'error')
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        flash('An error occurred. Please try again.', 'error')
    return redirect(url_for("index"))
    

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/home", methods=["POST",'GET'])
def home():
    config.clear_session()

    if request.method == "POST":
        input = bleach.clean(request.form.get("prompt"))
        questions = question_agent.getQuestion(input)
        config.initSessions(questions)
        logger.debug("All the sessions initialized")
        return redirect(url_for("quiz", question_id=1))

    return render_template("index.html")


@app.route("/questionPage/<int:question_id>", methods=["GET", "POST"])
def quiz(question_id):
    if "questions" not in session or not session["questions"]:
        return redirect(url_for("home"))

    current_questions = config.getQuestion(question_id)
    if not current_questions:
        return redirect(url_for("score"))


    if request.method == "POST":
        answer = request.form.get("answer")
        q_type = current_questions.get("Type", "mcq")
        question_key = str(question_id)

        is_duplicate_submission = question_key in session["user_answers"]
        
        if q_type == "mcq" or q_type == "true/false":
            if answer and not is_duplicate_submission:
                config.insert_answer(question_key,current_questions,answer,q_type)
                choosen_option_text = current_questions["Options"][int(answer) - 1]
                if current_questions["Correct"] == choosen_option_text:
                    if current_questions['QuestionNumber'] <= config.total_questions():
                        config.update_score()
                        config.update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],1)
                else:
                    config.update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],0)
        else:
            # For question type: text
            if not is_duplicate_submission:
                config.update_score()
                config.update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],1)
        logger.debug("User answer is recorded")
        return redirect(url_for("quiz", question_id=question_id + 1))

    template_name = "quizTEXT.html" if current_questions.get("Type", "mcq") == "text" else "quizMCQ.html"
    return render_template(
        template_name, questions=current_questions, total_questions=config.total_questions()
    )


@app.route("/score")
def score():
    ai_evaluation = eval_agent.evaluate(f"Questions: {session.get("questions", {})}\nUser Answers: {session.get("user_answers", {})}")
    return render_template(
        "evaluation.html",
        ai_evaluation=markdown.markdown(ai_evaluation),
        score=config.get_score(),
        total=config.total_questions(),
        performance=config.get_performance_metrics(),
    )



if __name__ == "__main__":
    logger.debug("Server Started")
    # app,db = main()
    app.run(debug=True, host="0.0.0.0")
