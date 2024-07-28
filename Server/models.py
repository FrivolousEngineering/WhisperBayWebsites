from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class GuestbookMessage(Base):
    __tablename__ = "guestbook_messages"
    id = Column(Integer, primary_key=True)
    author_name = Column(String, index=True)
    message = Column(String)
    target_board = Column(String, index=True)
    time = Column(String)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    text = Column(String)
    required = Column(Boolean)  # This indicates if the question can be changed via player interface
    type = Column(String)  # What type of question is it?

    answers = relationship("Answer", back_populates="question")
    options = relationship("QuestionOption", back_populates="question")


class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True)
    order = Column(Integer, default=0)
    value = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, index=True)
    value = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    articles = relationship("NewsArticle", back_populates="author")
    name = Column(String)
    password = Column(String)


class NewsArticle(Base):
    __tablename__ = "news_articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    time = Column(String)
    text = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="articles")


class ClubMembership(Base):
    __tablename__ = "club_membership"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    club_run_1 = Column(String)
    title_run_1 = Column(String)
    club_run_2 = Column(String)
    title_run_2 = Column(String)