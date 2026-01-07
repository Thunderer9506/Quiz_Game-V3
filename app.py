from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from agents.QuestionAgent import Agent, Question,QuestionList

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# agent = Agent()

questions = QuestionList(
    questions=[
    Question(
        QuestionNumber=1,
        Type="mcq",
        Category="technology",
        Question="Which version control system uses the .git directory?",
        Options=["Git", "Subversion", "Mercurial", "CVS"],
        Correct="Git",
        Difficulty="easy",
    ),
    Question(
        QuestionNumber=2,
        Type="true/false",
        Category="technology",
        Question='In Scrum, the "Product Owner" is responsible for writing unit tests.',
        Options=["True", "False"],
        Correct="False",
        Difficulty="medium",
    ),
    Question(
        QuestionNumber=3,
        Type="text",
        Category="technology",
        Question="Name the principle that states a module should have only one reason to change.",
        Options=[],
        Correct="Single Responsibility Principle",
        Difficulty="hard",
    ),
    Question(
        QuestionNumber=4,
        Type="mcq",
        Category="math",
        Question="What is the Big O notation for binary search on a sorted array of size n?",
        Options=["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        Correct="O(log n)",
        Difficulty="easy",
    ),
    Question(
        QuestionNumber=5,
        Type="true/false",
        Category="math",
        Question="The time complexity of merging two sorted lists of total length n is O(n^2).",
        Options=["True", "False"],
        Correct="False",
        Difficulty="medium",
    ),
    Question(
        QuestionNumber=6,
        Type="text",
        Category="math",
        Question="Provide the formula for the maximum number of edges in a directed acyclic graph with n vertices.",
        Options=[],
        Correct="n*(n-1)/2",
        Difficulty="hard",
    ),
    Question(
        QuestionNumber=7,
        Type="mcq",
        Category="science",
        Question="Which software development model emphasizes a sequential design process?",
        Options=["Waterfall", "Agile", "Spiral", "DevOps"],
        Correct="Waterfall",
        Difficulty="easy",
    ),
    Question(
        QuestionNumber=8,
        Type="true/false",
        Category="science",
        Question="The Spiral model incorporates risk analysis at each iteration.",
        Options=["True", "False"],
        Correct="True",
        Difficulty="medium",
    ),
    Question(
        QuestionNumber=9,
        Type="text",
        Category="science",
        Question="What is the name of the metric that measures the average number of defects per thousand lines of code?",
        Options=[],
        Correct="Defect Density",
        Difficulty="hard",
    ),
    Question(
        QuestionNumber=10,
        Type="mcq",
        Category="general",
        Question='What does "API" stand for?',
        Options=[
            "Application Programming Interface",
            "Automated Process Integration",
            "Advanced Protocol Interchange",
            "Applied Performance Index",
        ],
        Correct="Application Programming Interface",
        Difficulty="easy",
    ),
    Question(
        QuestionNumber=11,
        Type="true/false",
        Category="general",
        Question="RESTful APIs must always use JSON as the data format.",
        Options=["True", "False"],
        Correct="False",
        Difficulty="medium",
    ),
    Question(
        QuestionNumber=12,
        Type="text",
        Category="general",
        Question='In software licensing, what does the abbreviation "GPL" stand for?',
        Options=[],
        Correct="GNU General Public License",
        Difficulty="hard",
    ),
    Question(
        QuestionNumber=13,
        Type="mcq",
        Category="history",
        Question='Who is considered the "father of the Linux kernel"?',
        Options=[
            "Linus Torvalds",
            "Richard Stallman",
            "Dennis Ritchie",
            "Bjarne Stroustrup",
        ],
        Correct="Linus Torvalds",
        Difficulty="easy",
    ),
    Question(
        QuestionNumber=14,
        Type="true/false",
        Category="history",
        Question="The Agile Manifesto was published in 2001.",
        Options=["True", "False"],
        Correct="True",
        Difficulty="medium",
    ),
    Question(
        QuestionNumber=15,
        Type="text",
        Category="history",
        Question="What is the title of Steve McConnell's seminal book on software construction first published in 1993?",
        Options=[],
        Correct="Code Complete",
        Difficulty="hard",
    ),
]
)


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
        # input = request.form.get("prompt")
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
        q_type = current_questions.get("Type", "mcq")
        if q_type == "mcq" or q_type == "true/false":
            choosen_option_text = current_questions["Options"][int(answer) - 1]
            if current_questions["Correct"] == choosen_option_text:
                session["score"] = session.get("score", 0) + 1
                update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],1)
            else:
                update_performance_metrics(current_questions["Category"],current_questions["Difficulty"],0)
        else:
            # For text questions, just store the raw answer for now
            text_answers = session.get("text_answers", {})
            text_answers[str(questionId)] = answer
            session["text_answers"] = text_answers
            # Mark text questions as 0 for now (needs manual evaluation)
            update_performance_metrics(
                current_questions["Category"], current_questions["Difficulty"], 0
            )

        return redirect(url_for("quiz", questionId=questionId + 1))

    template_name = "quizTEXT.html" if q_type == "text" else "quizMCQ.html"
    return render_template(
        template_name, questions=current_questions, total_questions=session['total_questions']
    )


@app.route("/score")
def score():
    return render_template(
        "evaluation.html",
        score=session.get("score"),
        total=session['total_questions'],
        performance=session.get("performance_metrics", {}),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
