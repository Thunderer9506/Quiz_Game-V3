# ----------------------------------- Dependencies ------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_migrate import Migrate

from agents.QuestionAgent import Agent as QuestionAgent
from agents.EvaluationAgent import Agent as EvaluationAgent

from models import db
from schemas.user import User
from schemas.question import Question
from sqlalchemy import select

from route.payment import payment_bp
from route.auth import auth_bp
from utils.token_mangement import token_required, decode_jwt_token
from utils.session_management import create_session, update_session, total_questions, get_performance_metrics, update_performance_metrics, clear_session, insert_answer, update_score
from logger_config import logger

from dotenv import load_dotenv
import os
import markdown
import bleach
import uuid
import random

# ----------------------------------- Config ------------------------------------------

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(payment_bp)
app.register_blueprint(auth_bp)

migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)


if os.getenv("SECRET_KEY"):
    app.secret_key = os.getenv("SECRET_KEY")

question_agent = QuestionAgent()
eval_agent = EvaluationAgent()


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
            # Shuffle options randomly if they exist
            shuffled_options = question.Options.copy() if question.Options else []
            if shuffled_options:
                random.shuffle(shuffled_options)
            
            new_question = Question(
                id=str(uuid.uuid4()),
                session_id=session_id,
                question_number=question.QuestionNumber,
                question_text=question.Question,
                question_type=question.Type,
                category=question.Category,
                difficulty=question.Difficulty,
                options=shuffled_options,
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


# ----------------------------------- Routes ------------------------------------------



@app.route("/home", methods=["POST",'GET'])
@token_required
def home():
    stmt = select(User).where(User.id == decode_jwt_token(request.cookies.get("user_id")))
    user = db.session.execute(stmt).scalar()
    session["user_id"] = user.id

    if request.method == "POST":
        if user.credits < 1:
            flash("Not enough credits. Please purchase more credits.", "error")
            return redirect(url_for("home"))
        clear_session()
        input = bleach.clean(request.form.get("prompt"))
        session_id = str(uuid.uuid4())
        create_session(session_id, input)
        if create_question(session_id, input):
            user.credits = int(user.credits) - 1
            db.session.commit()
            question_ids = session.get("question_id", [])
            if not question_ids:
                flash("Failed to create quiz questions. Please try again.", "error")
                return redirect(url_for("home"))
            return redirect(url_for("quiz", question_id=question_ids[0]))
        else:
            flash("Failed to create quiz questions. Please try again.", "error")
            return redirect(url_for("home"))
        
    return render_template("index.html",user=user)


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
    
    ai_evaluation = eval_agent.evaluate(
        f"Questions: {session.get('questions', {})}\nUser Answers: {session.get('user_answers', {})}",
        session.get("session_id", "")
    )
    return render_template(
        "evaluation.html",
        ai_evaluation=markdown.markdown(ai_evaluation),
        score=session.get('score', 0),
        total=total_questions(),
        performance=get_performance_metrics(),
    )


# ----------------------------------- Global Error Handlers ------------------------------------------

def show_error_page(error_code, error_description):
    """Utility function to show error page with custom message"""
    logger.error(f"Manual Error Triggered: {error_code} - {error_description}")
    return render_template('error.html', error_no=error_code, error_desc=error_description), error_code

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    logger.error(f"404 Not Found: {request.url} - {error}")
    return render_template('error.html', error_no='404', error_desc='The page you are looking for does not exist.'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    logger.error(f"500 Internal Server Error: {request.url} - {error}")
    return render_template('error.html', error_no='500', error_desc='An internal server error occurred. Please try again later.'), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors"""
    logger.error(f"403 Forbidden: {request.url} - {error}")
    return render_template('error.html', error_no='403', error_desc='You do not have permission to access this resource.'), 403

@app.errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors"""
    logger.error(f"400 Bad Request: {request.url} - {error}")
    return render_template('error.html', error_no='400', error_desc='The server could not understand your request.'), 400

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled Exception: {request.url} - {type(error).__name__}: {str(error)}", exc_info=True)
    return render_template('error.html', error_no='500', error_desc='An unexpected error occurred. Please try again later.'), 500

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')