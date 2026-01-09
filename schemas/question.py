
from pydoc import text
from flask import json
from sqlalchemy.types import Integer, Text, JSON,String
from sqlalchemy.orm import Mapped, mapped_column
from models import db
from typing import Dict
import datetime

class Question(db.Model):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, nullable=False) #foreign key
    question_number: Mapped[int] = mapped_column(Integer)
    question_text: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    options: Mapped[json] = mapped_column(JSON)
    correct_answer: Mapped[str] = mapped_column(String)