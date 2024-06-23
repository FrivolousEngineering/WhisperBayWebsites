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
    return db.query(models.Question).filter(models.Question.id == question_id).first()


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


def create_question_option(db: Session, question_option: schemas.QuestionOptionCreate, question_id: int):
    db_question_option = models.QuestionOption(**question_option.dict(), question_id=question_id)
    # TODO: Ensure that the order of the option is unique
    db.add(db_question_option)
    db.commit()
    db.refresh(db_question_option)
    return db_question_option


def update_question_text(db:Session, question_id: int, new_text: str):
    db_question = get_question(db, question_id)
    db_question.text = new_text
    db.commit()


def update_question_type(db:Session, question_id: int, new_type: str):
    db_question = get_question(db, question_id)
    db_question.type = new_type
    db.commit()


def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int):
    db_answer = models.Answer(**answer.dict(), question_id=question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_question(db: Session, question_id: int):
    db_question = get_question(db, question_id)
    db.delete(db_question)
    db.commit()