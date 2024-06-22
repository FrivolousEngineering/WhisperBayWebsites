from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class GuestbookMessage(Base):
    __tablename__ = "guestbook_message"
    id = Column(Integer, primary_key=True)
    author_name = Column(String, index=True)
    message = Column(String)
    target_board = Column(String, index=True)