from flask import session
from models import db
from schemas.quiz_session import Sessions
from sqlalchemy import select
from logger_config import logger
import datetime


def create_session(session_id, title):
    try:
        user_id = session.get("user_id")
        if not user_id:
            logger.error("Missing user_id in session while creating session")
            return False
        new_session = Sessions(
            id= session_id, 
            user_id=user_id,
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
    try:
        stmt = select(Sessions).where(Sessions.id == session.get("session_id", ""))
        curr_session = db.session.execute(stmt).scalar()
        if not curr_session:
            logger.error("Session not found")
            return False
        curr_session.total_questions = total_questions()
        curr_session.score = session.get("score", 0)
        curr_session.status = "ended"
        curr_session.completed_at = datetime.datetime.now(datetime.timezone.utc)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error committing session update: {e}")
            return False
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating session: {e}")
        return False