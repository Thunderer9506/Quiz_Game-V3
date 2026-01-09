import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import db
from schemas.user import User
from schemas.quiz_session import Sessions
from schemas.question import Question

def test_simple():
    with app.app_context():
        try:
            # Test database connection
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Test creating a user
            user = User(
                id="test_user_001",
                email="test@example.com",
                password_hash="hashed_password",
                username="testuser"
            )
            db.session.add(user)
            db.session.commit()
            print("✅ User created successfully!")
            
            # Test creating a session
            session = Sessions(
                id="quiz_session_001",
                user_id="test_user_001",
                title="Test Quiz",
                total_questions=5,
                score=0,
                status="active"
            )
            db.session.add(session)
            db.session.commit()
            print("✅ Quiz session created successfully!")
            
            # Test creating a question
            question = Question(
                id = "question__001",
                session_id="quiz_session_001",
                question_number=1,
                question_text="What is 2+2?",
                question_type="mcq",
                category="math",
                difficulty="easy",
                options={"A": "3", "B": "4", "C": "5", "D": "6"},
                correct_answer="4"
            )
            db.session.add(question)
            db.session.commit()
            print("✅ Question created successfully!")
            
            # Test querying
            users = User.query.all()
            sessions = Sessions.query.all()
            questions = Question.query.all()
            
            print(f"📊 Found {len(users)} users, {len(sessions)} sessions, {len(questions)} questions")
            
            # Clean up
            db.session.delete(user)
            db.session.delete(session)
            db.session.delete(question)
            db.session.commit()
            print("🧹 Test data cleaned up")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple()