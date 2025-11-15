from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def home():
    questionPage = False
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            questionPage = True
    return render_template("index.html",questionPage = questionPage)

@app.route("/questionPage",methods=['GET','POST'])
def quiz():
    return render_template("quiz.html")

if __name__ == "__main__":
    app.run(debug=True)