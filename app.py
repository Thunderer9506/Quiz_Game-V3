from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from agents.QuestionAgent import Agent, Question,QuestionList
from agents.EvaluationAgent import Agent as EvaluationAgent
import markdown 

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

question_agent = Agent()

eval_agent = EvaluationAgent()


def initialize_performance_metrics():
    return {"category": {}, "difficulty": {"easy": [], "medium": [], "hard": []}}


def update_performance_metrics(category, difficulty, score):
    if category not in session["performance_metrics"]["category"]:
        session["performance_metrics"]["category"][category] = [score]
    else:
        session["performance_metrics"]["category"][category].append(score)

    session["performance_metrics"]["difficulty"][difficulty].append(score)


def clear_performance_metrics():
    if "performance_metrics" in session:
        session.pop("performance_metrics")


@app.route("/", methods=["GET", "POST"])
def home():
    session.clear()
    clear_performance_metrics()

    if request.method == "POST":
        input = request.form.get("prompt")
        questions = question_agent.getQuestion(input)
        session["score"] = 0
        session["questions"] = questions.model_dump()
        session['total_questions'] = len(session['questions']['questions'])
        session["performance_metrics"] = initialize_performance_metrics()
        return redirect(url_for("quiz", questionId=1))

    return render_template("index.html")


@app.route("/questionPage/<int:questionId>", methods=["GET", "POST"])
def quiz(questionId):
    if questionId > session['total_questions']:
        return redirect(url_for("score"))

    # What if the user bookmarked this page, questions wont be present
    # in session giving us errors
    if "questions" not in session or not session["questions"]:
        return redirect(url_for("home"))

    current_questions = session["questions"]["questions"][questionId - 1]

    if request.method == "POST":
        answer = request.form.get("answer")
        
        # Store all user answers (MCQ, true/false, text)
        user_answers = session.get("user_answers", {})
        q_type = current_questions.get("Type", "mcq")
        
        # Check if this question was already answered to prevent cheating
        question_key = str(questionId)
        is_duplicate_submission = question_key in user_answers
        
        user_answers[question_key] = {
            "question": current_questions["Question"],
            "user_answer": answer,
            "correct_answer": current_questions["Correct"],
            "type": q_type,
            "category": current_questions["Category"],
            "difficulty": current_questions["Difficulty"]
        }
        session["user_answers"] = user_answers
        
        if q_type == "mcq" or q_type == "true/false":
            if answer and not is_duplicate_submission:  # Only score if not duplicate
                choosen_option_text = current_questions["Options"][int(answer) - 1]
                if current_questions["Correct"] == choosen_option_text:
                    if current_questions['QuestionNumber'] <= session['total_questions']:
                        session["score"] = session.get("score", 0) + 1
                        update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],1)
                else:
                    update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],0)
        else:
            # For text questions, only update metrics if not duplicate submission
            if not is_duplicate_submission:
                update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],0)

        return redirect(url_for("quiz", questionId=questionId + 1))

    template_name = "quizTEXT.html" if current_questions.get("Type", "mcq") == "text" else "quizMCQ.html"
    return render_template(
        template_name, questions=current_questions, total_questions=session['total_questions']
    )


@app.route("/score")
def score():
    ai_evaluation = eval_agent.evaluate(f"Questions: {session.get("questions", {})}\nUser Answers: {session.get("user_answers", {})}")
    return render_template(
        "evaluation.html",
        ai_evaluation=markdown.markdown(ai_evaluation),
        score=session.get("score"),
        total=session['total_questions'],
        performance=session.get("performance_metrics", {}),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
