from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models import db
import datetime

class Sessions(db.Model):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String)
    total_questions: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))