from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import db
import datetime

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String,primary_key=True)
    email: Mapped[str] = mapped_column(String,unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String,unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))
    
    # Relationships
    sessions: Mapped[list["Sessions"]] = relationship("Sessions", back_populates="user", cascade="all, delete-orphan")