import html

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from . import models, schemas

def get_guestbook_message_for_board(db: Session, board: str):
    return db.query(models.GuestbookMessage).filter(models.GuestbookMessage.target_board == board)


def create_guestbook_message(db: Session, message: schemas.GuestbookMessageCreate):
    db_message = models.GuestbookMessage(**message.dict())
    db_message.message = html.escape(db_message.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_questions(db: Session):
    return db.query(models.Question).order_by(models.Question.order)


def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id)


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**question.dict())
    if question.order is None:  # If no order is set, set it to the highest number +1
        highest_order = db.query(func.max(models.Question.order)).scalar()
        if highest_order is None:
            highest_order = -1  # That way we will use 0 in the next one
        db_question.order = highest_order + 1
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question