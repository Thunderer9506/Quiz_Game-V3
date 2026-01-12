from sqlalchemy import Integer, Text, JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import db
from typing import List

class Question(db.Model):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id"), nullable=False)
    question_number: Mapped[int] = mapped_column(Integer)
    question_text: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    options: Mapped[List[str]] = mapped_column(JSON)
    correct_answer: Mapped[str] = mapped_column(String)
    
    # Relationships
    session: Mapped["Sessions"] = relationship("Sessions", back_populates="questions")