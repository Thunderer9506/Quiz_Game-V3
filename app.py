from flask import Flask,render_template,request,redirect,url_for,session
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


STATIC_QUESTIONS = [
    {
        "id": 1,
        "type": "mcq",
        "category": "General",
        "question": "What does HTTP stand for?",
        "options": [
            "HyperText Transfer Protocol",
            "High Transfer Text Protocol",
            "Hyperlink Transfer Protocol",
            "HyperText Transmission Program"
        ],
        "correct": "HyperText Transfer Protocol",
        "difficulty": "easy"
    },
    {
        "id": 2,
        "type": "mcq",
        "category": "Science",
        "question": "Which gas is most abundant in Earth’s atmosphere?",
        "options": [
            "Oxygen",
            "Nitrogen",
            "Carbon Dioxide",
            "Argon"
        ],
        "correct": "Nitrogen",
        "difficulty": "easy"
    },
    {
        "id": 3,
        "type": "text",
        "category": "Math",
        "question": "Define the Pythagorean theorem.",
        "options": [],
        "correct": None,
        "difficulty": "medium"
    },
    {
        "id": 4,
        "type": "mcq",
        "category": "History",
        "question": "Who was the first President of the United States?",
        "options": [
            "George Washington",
            "Thomas Jefferson",
            "John Adams",
            "James Madison"
        ],
        "correct": "George Washington",
        "difficulty": "easy"
    },
    {
        "id": 5,
        "type": "text",
        "category": "Technology",
        "question": "Explain what an API is and give one real-world example.",
        "options": [],
        "correct": None,
        "difficulty": "medium"
    },
]

def initialize_performance_metrics():
    return {
    "category": {},
    "difficulty": {
        'easy': [],
        'medium': [],
        'hard': []
    }
}

def update_performance_metrics(category, difficulty, score):
    if category not in session['performance_metrics']['category']:
        session['performance_metrics']['category'][category] = [score]
    else:
        session['performance_metrics']['category'][category].append(score)

    session['performance_metrics']['difficulty'][difficulty].append(score)

def clear_performance_metrics():
    if 'performance_metrics' in session:
        session.pop('performance_metrics')


@app.route("/",methods=['GET','POST'])
def home():
    session.clear()
    clear_performance_metrics()

    if request.method == 'POST':
        # input = request.form.get('prompt')
        session['score'] = 0
        session['questions'] = STATIC_QUESTIONS
        session['performance_metrics'] = initialize_performance_metrics()
        return redirect(url_for('quiz',questionId = 1))
        
    return render_template("index.html")

@app.route("/questionPage/<int:questionId>",methods=['GET','POST'])
def quiz(questionId):
    # What if the user bookmarked this page, questions wont be present
    # in session giving us errors
    if 'questions' not in session or not session['questions']:
        return redirect(url_for('home'))
    
    all_questions = session['questions']
    
    if questionId >= len(all_questions):
        return redirect(url_for('score'))
    
    current_questions = all_questions[questionId-1]
    q_type = current_questions.get('type', 'mcq')

    if request.method == 'POST':
        answer = request.form.get('answer')
        if q_type == 'mcq':
            if answer:
                choosen_option_text = current_questions['options'][int(answer)-1]
                if current_questions['correct'] == choosen_option_text:
                    session['score'] = session.get('score',0)+1
                    update_performance_metrics(current_questions['category'], current_questions['difficulty'], 1)
                else:
                    update_performance_metrics(current_questions['category'], current_questions['difficulty'], 0)
        else:
            # For text questions, just store the raw answer for now
            text_answers = session.get('text_answers', {})
            text_answers[str(questionId)] = answer
            session['text_answers'] = text_answers
            # Mark text questions as 0 for now (needs manual evaluation)
            update_performance_metrics(current_questions['category'], current_questions['difficulty'], 0)

        return redirect(url_for('quiz',questionId = questionId + 1))

    template_name = "quizMCQ.html" if q_type == "mcq" else "quizTEXT.html"
    return render_template(template_name,questions = current_questions,total_questions = len(all_questions))

@app.route("/score")
def score():
    return render_template("evaluation.html",score = session.get('score'),
                                        total = len(session.get('questions',[])),
                                        performance = session.get('performance_metrics', {}))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')