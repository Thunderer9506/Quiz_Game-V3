from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import db
import datetime

class Sessions(db.Model):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String)
    total_questions: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer,default=0)
    status: Mapped[str] = mapped_column(String,default="active")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="session", cascade="all, delete-orphan")