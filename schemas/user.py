from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models import db
import datetime

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String,primary_key=True)
    email: Mapped[str] = mapped_column(String,unique=True, index=True)
    username: Mapped[str] = mapped_column(String,unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,default=datetime.datetime.now(datetime.timezone.utc))