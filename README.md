# 🚀 Flask Quiz App

A dynamic, full-stack quiz application built with Flask and Python. This app allows users to select a quiz category, difficulty, and type, then fetches questions from an external API, tracks their score, and displays the final result.

The project features a clean, modern, and responsive UI with a CSS-only light/dark mode toggle.

### Demo Link

**[View Live Demo](https://quiz-game-v3.onrender.com/)**

---

### 📸 Screenshots

#### 1. Home Page (Quiz Setup)
The user selects their quiz options from the dropdowns.
![Home Page](/Screenshot/Home%20Page.png)


#### 2. Quiz Page (Question)
The user answers a question. The UI is clean, and the radio buttons are custom-styled.
![Quiz Page](/Screenshot/Quiz%20Page.png)


#### 3. Score Page (Results)
The final score is displayed, and the user can choose to play again.
![Score Page](/Screenshot/Score%20Page.png)


---

## ✨ Features

* **Dynamic Quiz Generation:** Fetches questions (from the Open Trivia Database via `generateQuestion.py`) based on user-selected category, difficulty, and question type.
* **CSS-Only Theme Toggle:** A smooth light/dark mode switch built entirely with CSS variables and a hidden checkbox, requiring no JavaScript.
* **Secure Session Management:** Uses Flask's server-side `session` to securely track each user's quiz questions and score, allowing for multiple users at the same time.
* **Responsive Design:** The UI is fully responsive and works on all device sizes.
* **Clean Code Structure:** The backend logic is separated from the frontend, and the CSS is modularized into a `base.css` and page-specific files (`home.css`, `quiz.css`, `score.css`).

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3 (using CSS Variables and Flexbox)
* **API:** Open Trivia Database (assumed)
* **Icons:** Font Awesome

---

## 🚀 Getting Started

To run this project on your local machine, follow these steps.

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/Thunderer9506/Quiz_Game-V3](https://github.com/Thunderer9506/Quiz_Game-V3)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    * **Windows:**
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    (You'll need a `requirements.txt` file for this. Based on our code, it should contain `Flask` and `requests`.)
    ```sh
    pip install Flask requests
    ```

4.  **Set the Flask Secret Key:**
    In `app.py`, change the `app.secret_key` to your own random, secure string:
    ```python
    # In app.py
    app.secret_key = 'your-own-very-secret-key'
    ```

5.  **Run the application:**
    ```sh
    flask run
    ```
    Or in debug mode:
    ```sh
    python app.py
    ```

6.  Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 🙏 Acknowledgements & Inspiration

This project's design and structure were inspired by the following repositories.
*(Please add the links to the two repos you mentioned.)*

* **[Quiz-Game-V2](https://github.com/Thunderer9506/Quiz_Game-V2)**
* **[Quiz-Game-Webpage](https://github.com/Thunderer9506/Quiz-App.github.io)**
