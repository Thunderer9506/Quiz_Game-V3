# 🚀 AI-Powered Quiz Game V3

A modern, full-stack quiz application powered by AI that generates dynamic questions, manages user authentication, handles payments, and provides a complete quiz experience with real-time evaluation.

## 📹 Video Demo

Check out the complete demo video to see the app in action:

![Video title](./Demo/Quiz%20App%20Demo.gif)

---

## ✨ Features

### 🤖 AI-Powered Question Generation
- **Dynamic Quiz Creation**: Uses LangChain with Groq AI to generate contextual questions based on user prompts
- **Multiple Question Types**: Supports MCQ, True/False, and Text-based questions
- **Smart Evaluation**: AI-powered evaluation and feedback on user answers
- **Performance Metrics**: Tracks user performance by category and difficulty

### 🔐 Complete User Management
- **Secure Authentication**: JWT-based login/signup system with Argon2 password hashing
- **Session Management**: Secure server-side session handling
- **Credit System**: Users purchase credits to take quizzes
- **Profile Management**: User dashboard with credit tracking

### 💳 Payment Integration
- **Razorpay Integration**: Complete payment gateway for credit purchases
- **Secure Transactions**: Webhook-based payment verification
- **Flexible Pricing**: User can choose as many credits as it wants
- **Real-time Credit Updates**: Instant credit addition after successful payment

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Mode**: CSS-only theme toggle with smooth transitions
- **Interactive Quiz Interface**: Engaging question display with difficulty indicators
- **Error Handling**: Comprehensive error pages with user-friendly messages

### 🏗️ Robust Architecture
- **Modular Structure**: Clean separation of concerns with blueprints
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Logging System**: Comprehensive error logging and monitoring
- **API Security**: Token-based route protection

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask with Python 3.12+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with Argon2 password hashing
- **AI Integration**: LangChain with Groq API
- **Payment**: Razorpay payment gateway
- **Migration**: Flask-Migrate for database versioning

### Frontend
- **Templates**: Jinja2 with modern HTML5
- **Styling**: CSS3 with CSS Variables and Flexbox
- **Icons**: Font Awesome
- **Responsive**: Mobile-first design approach

### Development Tools
- **Package Management**: pyproject.toml with modern Python packaging
- **Environment**: dotenv for configuration management
- **Logging**: Python logging with file and console handlers
- **Error Handling**: Global exception handlers with custom error pages

---

## 📁 Project Structure

```
Quiz_Game-V3/
├── agents/                 # AI agents for question generation and evaluation
│   ├── QuestionAgent.py    # Handles question generation
│   └── EvaluationAgent.py  # Handles answer evaluation
├── route/                  # Flask blueprints
│   ├── auth.py            # Authentication routes
│   └── payment.py         # Payment processing routes
├── utils/                  # Utility functions
│   ├── token_mangement.py # JWT token handling
│   └── session_management.py # Session utilities
├── schemas/               # Database models
│   ├── user.py           # User model
│   ├── question.py       # Question model
│   └── quiz_session.py   # Session model
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── templates/           # HTML templates
├── migrations/          # Database migrations
├── Demo/               # Demo video
└── app.py             # Main application file
```

---

## 🎯 How It Works

1. **User Registration**: Users create accounts with secure password hashing
2. **Credit Purchase**: Users buy credits using Razorpay payment gateway
3. **Quiz Generation**: Users input prompts, AI generates contextual questions
4. **Interactive Quiz**: Users answer questions with real-time feedback
5. **AI Evaluation**: AI evaluates answers and provides detailed feedback
6. **Performance Tracking**: System tracks performance metrics and progress

---

## 🔧 Configuration

### AI Model Configuration
- Default model: `llama3-70b-8192`
- Configurable via `GROQ_MODEL` environment variable
- Supports temperature and other model parameters

### Payment Configuration
- Test mode: Use Razorpay test keys for development
- Live mode: Use production keys for deployment
- Webhook URL: Configure for payment confirmations

### Database Configuration
- Supports PostgreSQL with connection pooling
- Automatic migrations with Flask-Migrate
- Session management with secure cookies

---



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 🆘 Support

For support, please:
1. Check the demo video for common workflows
2. Review the error logs in `mainApp.log`
3. Create an issue with detailed information
4. Include environment details and error messages

---

**Built with ❤️ using Flask, AI, and modern web technologies**

