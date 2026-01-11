# ----------------------------------- Dependencies ------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_migrate import Migrate

from agents.QuestionAgent import Agent as QuestionAgent
from agents.EvaluationAgent import Agent as EvaluationAgent

from models import db
from schemas.user import User
from schemas.question import Question
from schemas.quiz_session import Sessions
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from dotenv import load_dotenv
import os
import markdown
import logging
import bleach
import uuid
import datetime
import argon2
import jwt
import datetime as dt
from functools import wraps

# ----------------------------------- Config ------------------------------------------

load_dotenv()

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
ph = argon2.PasswordHasher()

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24*7

# Create and configure logger
logging.basicConfig(filename="mainApp.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

# ----------------------------------- Usefull Functions ------------------------------------------

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("user_id")
        if not token:
            return redirect(url_for("index"))
        
        try:
            user_id = decode_jwt_token(token)
            if not user_id:
                return redirect(url_for("index"))
        except:
            return redirect(url_for("index"))
        
        # Add user to request context
        return f(*args, **kwargs)
    return decorated

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def create_session(session_id, title):
    try:
        new_session = Sessions(
            id= session_id, 
            user_id= session["user_id"],
            title = title,
            total_questions=0  # Will be updated later
            )
        if new_session:
            db.session.add(new_session)
            db.session.commit()
            session["session_id"] = session_id
            logger.debug(f"New session created: {session_id}")
            return True
    except Exception as e:
        logger.error(f"Encountered error while creating session: {e}")
        return False

def create_question(session_id, input):
    """Create a new quiz session with questions"""
    try:
        # Get questions from AI agent
        questions = question_agent.getQuestion(input, session_id)
        logger.debug(f"AI Response: {questions}")
        logger.debug(f"Questions type: {type(questions)}")
        if hasattr(questions, 'questions'):
            logger.debug(f"Questions.questions: {questions.questions}")
            logger.debug(f"Number of questions: {len(questions.questions)}")
        
        # Store session info in Flask session
        session['session_id'] = session_id
        session['question_id'] = []
        
        # Create questions
        for question in questions.questions:
            new_question = Question(
                id=str(uuid.uuid4()),
                session_id=session_id,
                question_number=question.QuestionNumber,
                question_text=question.Question,
                question_type=question.Type,
                category=question.Category,
                difficulty=question.Difficulty,
                options=question.Options,
                correct_answer=question.Correct,
            )
            db.session.add(new_question)
            session['question_id'].append(new_question.id)
            logger.debug(f"Question {question.QuestionNumber} added successfully")
        
        db.session.commit()
        logger.debug("All questions added successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating question session: {e}")
        db.session.rollback()
        return False
    
def total_questions():
    """Get total questions from session"""
    try:
        question_ids = session.get('question_id', [])
        return len(question_ids) if question_ids else 0
    except Exception as e:
        logger.error(f"Error getting total questions: {e}")
        return 0

def get_performance_metrics():
    """Get performance metrics from session"""
    try:
        return session.get('performance_metrics', {
            "category": {},
            "difficulty": {"easy": [], "medium": [], "hard": []}
        })
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return {
            "category": {},
            "difficulty": {"easy": [], "medium": [], "hard": []}
        }

def update_performance_metrics(category, difficulty, score):
    """Update performance metrics in session"""
    try:
        metrics = session.get('performance_metrics', {
            "category": {},
            "difficulty": {"easy": [], "medium": [], "hard": []}
        })
        
        # Update category metrics
        if category not in metrics["category"]:
            metrics["category"][category] = [score]
        else:
            metrics["category"][category].append(score)
        
        # Update difficulty metrics
        if difficulty in metrics["difficulty"]:
            metrics["difficulty"][difficulty].append(score)
        else:
            metrics["difficulty"][difficulty] = [score]
        
        session["performance_metrics"] = metrics
    except Exception as e:
        logger.error(f"Error updating performance metrics: {e}")

def clear_session():
    """Clear session data"""
    try:
        session["score"] = 0
        session["performance_metrics"] = {
            "category": {},
            "difficulty": {"easy": [], "medium": [], "hard": []}
        }
        session["curr_question"] = 0
        session["user_answers"] = {}
    except Exception as e:
        logger.error(f"Error clearing session: {e}")

def insert_answer(question_key, current_question, answer, q_type):
    """Insert user answer into session"""
    try:
        user_answers = session.get("user_answers", {})
        user_answers[question_key] = {
            "question": current_question.get("Question", ""),
            "user_answer": answer,
            "correct_answer": current_question.get("Correct", ""),
            "type": q_type,
            "category": current_question.get("Category", ""),
            "difficulty": current_question.get("Difficulty", "")
        }
        session["user_answers"] = user_answers
    except Exception as e:
        logger.error(f"Error inserting answer: {e}")

def update_score():
    """Update user score in session"""
    try:
        current_score = session.get("score", 0)
        if isinstance(current_score, int):
            session["score"] = current_score + 1
        else:
            logger.warning(f"Invalid score type: {type(current_score)}")
            session["score"] = 1  # Reset to 1 if invalid type
    except Exception as e:
        logger.error(f"Error updating score: {e}")
        session["score"] = 1

def update_session():
    stmt = select(Sessions).where(Sessions.id == session.get("session_id",""))
    curr_session = db.session.execute(stmt).scalar()
    curr_session.total_questions = total_questions()
    curr_session.score = session.get("score",0)
    curr_session.status = "ended"
    curr_session.completed_at = datetime.datetime.now(datetime.timezone.utc)
    db.session.commit()

# ----------------------------------- Routes ------------------------------------------

@app.route("/")
def index():
    return render_template("auth.html")

@app.post("/login")
def login():
    clear_session()
    email = request.form.get("email")
    password = request.form.get("password")
    stmt = select(User).where(User.email == email)
    user = db.session.execute(stmt).scalar()
    if user:
        if ph.verify(user.password_hash,password):
            logger.info(f"User {user.username} logged in successfully")
            session["user_id"] = user.id
            token = generate_jwt_token(user.id)
            response = make_response(redirect(url_for("home")))
            response.set_cookie('user_id', token)
            return response
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
        new_user = User(id=str(uuid.uuid4()),username=str(username),email=str(email),password_hash=str(ph.hash(password)))
        db.session.add(new_user)
        db.session.commit()
        
        session["user_id"] = new_user.id
        return redirect(url_for("index"))

    except IntegrityError as e:
        logger.error(f"User already exist {e}")
        flash('User already Exist', 'error')
        
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        flash('An error occurred. Please try again.', 'error')
        
    return redirect(url_for("index"))
    
@app.get("/logout")
@token_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/home", methods=["POST",'GET'])
@token_required
def home():
    if request.method == "POST":
        clear_session()
        input = bleach.clean(request.form.get("prompt"))
        session_id = str(uuid.uuid4())
        create_session(session_id, input)
        if create_question(session_id, input):
            return redirect(url_for("quiz",question_id = session["question_id"][0]))
        else:
            flash("Failed to create quiz questions. Please try again.", "error")
            return redirect(url_for("home"))
        
    return render_template("index.html")


@app.route("/questionPage/<string:question_id>", methods=["GET", "POST"])
@token_required
def quiz(question_id):
    """Handle quiz questions"""
    try:
        # Get question from database
        stmt = select(Question).where(Question.id == question_id)
        question = db.session.execute(stmt).scalar()
        if not question:
            logger.warning(f"Question not found: {question_id}")
            return redirect(url_for("home"))
        
        logger.debug(f"Retrieved question: {question.id}")
        
        
        # Prepare question data for template
        current_question = {
            "QuestionNumber": question.question_number,
            "Question": question.question_text,
            "Type": question.question_type,
            "Category": question.category,
            "Difficulty": question.difficulty,
            "Options": question.options,
            "Correct": question.correct_answer
        }

        # Determine template based on question type
        q_type = current_question.get("Type", "mcq")
        template_name = "quizTEXT.html" if q_type == "text" else "quizMCQ.html"

        # Handle form submission
        if request.method == "POST":
            answer = request.form.get("answer")
            question_key = str(current_question["QuestionNumber"])  # Convert to string for session key

            # Check for duplicate submission
            user_answers = session.get("user_answers", {})
            is_duplicate_submission = question_key in user_answers
            
            if answer and not is_duplicate_submission:
                # Handle scoring based on question type
                if q_type in ["mcq", "true/false"]:
                    try:
                        answer_index = int(answer) - 1
                        options = current_question.get("Options", [])
                        if 0 <= answer_index < len(options):
                            choosen_option_answer = options[answer_index]
                        else:
                            choosen_option_answer = answer
                    except (ValueError, TypeError):
                        choosen_option_answer = answer
                    
                    if current_question.get("Correct") == choosen_option_answer:
                        update_score()
                        update_performance_metrics(
                            current_question.get("Category", ""), 
                            current_question.get("Difficulty", ""), 
                            1
                        )
                    else:
                        # Incorrect answer - still update performance metrics with score 0
                        update_performance_metrics(
                            current_question.get("Category", ""), 
                            current_question.get("Difficulty", ""), 
                            0
                        )
                else:
                    choosen_option_answer = answer
                    # For text questions
                    update_score()
                    update_performance_metrics(
                        current_question.get("Category", ""), 
                        current_question.get("Difficulty", ""), 
                        1
                    )
                
                insert_answer(question_key, current_question, choosen_option_answer, q_type)
                logger.debug("User answer recorded")
                
                # Get next question
                question_ids = session.get("question_id", [])
                current_index = session.get("curr_question", 0)
                
                if current_index + 1 < len(question_ids):
                    next_question_id = question_ids[current_index + 1]
                    session["curr_question"] = current_index + 1
                    return redirect(url_for("quiz", question_id=next_question_id))
                else:
                    return redirect(url_for("score"))
            else:
                logger.warning("Duplicate submission detected")

        return render_template(
            template_name, 
            questions=current_question, 
            total_questions=total_questions()
        )
        
    except Exception as e:
        logger.error(f"Error in quiz route: {e}")
        return redirect(url_for("home"))


@app.route("/score")
@token_required
def score():
    update_session()
    
    ai_evaluation = eval_agent.evaluate(f"Questions: {session.get("questions", {})}\nUser Answers: {session.get("user_answers", {})}")
    return render_template(
        "evaluation.html",
        ai_evaluation=markdown.markdown(ai_evaluation),
        score=session['score'],
        total=total_questions(),
        performance=get_performance_metrics(),
    )

if __name__ == "__main__":
    logger.debug("Server Started")
    app.run(debug=True, host="0.0.0.0")
