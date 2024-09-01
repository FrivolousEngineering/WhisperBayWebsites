from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Prediction(Base):
    __tablename__ = 'predicitions'
    id = Column(Integer, primary_key=True)
    severity = Column(Integer)
    text = Column(String)
    # TODO; I should probably not have cut certain corners that I did, but here we are. I didn't put characters in the DB
    # Correctly, so now it's just linking em via firstname, which is also unique, but far from elegant
    first_name = Column(String)


class PredictionDirection(Base):
     __tablename__ = 'predicition_direction'
     id = Column(Integer, primary_key=True)
     individual_vs_collectivist = Column(String, default = "neutral")
     agnostic_vs_spiritual = Column(String, default = "neutral")
     progressive_vs_conservative = Column(String, default = "neutral")


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

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    options = relationship("QuestionOption", back_populates="question")


class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True)
    order = Column(Integer, default=0)
    value = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")


class RunState(Base):
    __tablename__ = "run_state"
    id = Column(Integer, primary_key=True)
    escalation_level = Column(Integer, default = 0)


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, index=True)
    value = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
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