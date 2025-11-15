let stateMode = 0
const icons = {
    'Html': {
        class: 'fa-solid fa-code',
        style: 'background-color: #FFF1E9; color: orange;'
    },
    'Css': {
        class: 'fa-solid fa-brush',
        style: 'background-color: #E0FDEF; color: green;'
    },
    'Js': {
        class: 'fa-brands fa-js',
        style: 'background-color: #EBF0FF; color: blue;'
    },
    'Accessibility': {
        class: 'fa-solid fa-person',
        style: 'background-color: #F6E7FF; color: purple;'
    }
}
const choice = document.querySelectorAll(".choice")
const subjects = document.querySelectorAll(".subjects Button")
const form = document.querySelector("form")
const options = document.querySelectorAll(".options Button")
const optionArr = Array.from(options).slice(0,4)
let subject = ""
let option = ""
let questionNumber = 1
let score = 0

function switchMode(){
    if (stateMode == 0) {
        console.log("Dark Mode on");
        document.body.style.backgroundColor = "#313E51"
        document.body.style.color = "#fff"
        choice.forEach(element => {
            element.style.backgroundColor = "#fff"
            element.style.color = "#3B4D66"
        });
        stateMode = 1
    } else{
        console.log("Lign Mode on");
        document.body.style.backgroundColor = "#fff"
        document.body.style.color = "#313E51"
        choice.forEach(element => {
            element.style.backgroundColor = "#3B4D66"
            element.style.color = "#fff"
        });
        stateMode = 0
    }
}

function renderQuestionpage(){
    document.querySelector('.subjectIcon').innerHTML = 
    `<i class="${icons[subject].class}"
        style="${icons[subject].style}"></i>
    <h2>${subject}</h2>`
    const questionNo = document.querySelector('.questionNo')
    const question = document.querySelector('.question')
    const option1 = document.querySelector('.option-1')
    const option2 = document.querySelector('.option-2')
    const option3 = document.querySelector('.option-3')
    const option4 = document.querySelector('.option-4')
    questionNo.textContent = `Question ${questionNumber} of 10`
    question.textContent = quizData[subject][0]['question']
    option1.textContent = quizData[subject][0]['options'][0]
    option2.textContent = quizData[subject][0]['options'][1]
    option3.textContent = quizData[subject][0]['options'][2]
    option4.textContent = quizData[subject][0]['options'][3]
}

function getsubjectValue(){
    subjects.forEach((ele, key) => {
        ele.addEventListener("click", () => {
            subject = ele['childNodes'][3].textContent
            document.querySelector('.container').style.display = 'none'
            document.querySelector('.questionPage').style.display = 'block'
            renderQuestionpage()
            formHandling()
        })
    })
}

function userChose(){
    optionArr.forEach((ele, key) => {
        ele.addEventListener("click", () => {
            optionArr.forEach(btn => btn.classList.remove('active'));
            ele.classList.add('active');
            option = ele.querySelector('p').textContent;
            console.log(option);
            
        })
    })
}

function renderNextQuestion(){
    const questionNo = document.querySelector('.questionNo')
    const question = document.querySelector('.question')
    const option1 = document.querySelector('.option-1')
    const option2 = document.querySelector('.option-2')
    const option3 = document.querySelector('.option-3')
    const option4 = document.querySelector('.option-4')
    questionNo.textContent = `Question ${questionNumber} of 10`
    question.textContent = quizData[subject][questionNumber-1]['question']
    option1.textContent = quizData[subject][questionNumber-1]['options'][0]
    option2.textContent = quizData[subject][questionNumber-1]['options'][1]
    option3.textContent = quizData[subject][questionNumber-1]['options'][2]
    option4.textContent = quizData[subject][questionNumber-1]['options'][3]
    optionArr.forEach(btn => btn.classList.remove('active'));
}

function renderScoreBoard(){
    document.querySelector('.questionPage').style.display = 'none'
    document.querySelector('.ScoreBoard').style.display = 'block'
    document.querySelector('.score-value').innerHTML = `${score} <span>/ 10</span>`
}

function formHandling(){
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const answer = quizData[subject][questionNumber-1]["answer"];
        if (answer == option){
            score += 1;
            alert("Right Answer");
        } else{
            alert("Wrong Answer");
            if (score > 0){
                score -= 1;
            }
        }
        if (questionNumber != 10){
            questionNumber += 1;
            renderNextQuestion();
        } else{
            renderScoreBoard()
        }
    });
}
function restart(){
    stateMode = 0
    subject = ""
    option = ""
    questionNumber = 1
    score = 0
    document.querySelector('.ScoreBoard').style.display = 'none'
    document.querySelector('.container').style.display = 'block'
    getsubjectValue()
    userChose()
}

getsubjectValue()
userChose()
