import html

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from . import models, schemas


def get_guestbook_message_for_board(db: Session, board: str):
    return db.query(models.GuestbookMessage).filter(models.GuestbookMessage.target_board == board)


def create_guestbook_message(db: Session, message: schemas.GuestbookMessageCreate):
    time = datetime.now()
    time = time.replace(year=1991)

    return create_guestbook_message_custom_time(db=db, message=message, custom_time=time.strftime("%Y-%m-%d %H:%M"))


def create_guestbook_message_custom_time(db: Session, message: schemas, custom_time: str):
    db_message = models.GuestbookMessage(**message.dict(), time=custom_time)
    db_message.message = html.escape(db_message.message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_questions(db: Session):
    return db.query(models.Question).order_by(models.Question.order)


def get_question_option(db: Session, option_id: int):
    return db.query(models.QuestionOption).filter(models.QuestionOption.id == option_id).first()


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


def update_question_text(db: Session, question_id: int, new_text: str):
    db_question = get_question(db, question_id)
    db_question.text = new_text
    db.commit()


def update_question_type(db: Session, question_id: int, new_type: str):
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


def delete_option(db: Session, option_id: int):
    db_question_option = get_question_option(db, option_id)
    db.delete(db_question_option)
    db.commit()


def update_option_text(db:Session, option_id: int, new_text: str):
    db_question_option = get_question_option(db, option_id)
    db_question_option.value = new_text
    db.commit()


def reset_database(db: Session):
    db.query(models.Answer).delete()
    db.query(models.Question).delete()
    db.query(models.QuestionOption).delete()
    db.commit()


def seed_database(db: Session):
    # Add the default stuff in the datbase
    create_question(db, schemas.QuestionCreate(text="What is your name?", type="freeform", required=True))
    create_question(db, schemas.QuestionCreate(text="What is your age?", type="pickone", required=True))
    create_question(db, schemas.QuestionCreate(text="What is your gender?", type="pickone", required=True))
    create_question(db, schemas.QuestionCreate(text="What is your marital status?", type="pickone", required=True))

    # Age brackets
    create_question_option(db, schemas.QuestionOptionCreate(value="18 to 24"), 2)
    create_question_option(db, schemas.QuestionOptionCreate(value="25 to 34"), 2)
    create_question_option(db, schemas.QuestionOptionCreate(value="35 to 44"), 2)
    create_question_option(db, schemas.QuestionOptionCreate(value="45 to 54"), 2)
    create_question_option(db, schemas.QuestionOptionCreate(value="55 to 64"), 2)
    create_question_option(db, schemas.QuestionOptionCreate(value="65+"),      2)

    # Gender
    create_question_option(db, schemas.QuestionOptionCreate(value="Male"), 3)
    create_question_option(db, schemas.QuestionOptionCreate(value="Female"), 3)

    # Marital status
    create_question_option(db, schemas.QuestionOptionCreate(value="Single"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Married"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Widowed"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Divorced"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Separated"), 4)

    # Add some of the not required questions
    create_question(db, schemas.QuestionCreate(text="It is impossible to stay faithful to one’s spouse for 40 years", type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 5)

    create_question(db, schemas.QuestionCreate(text="It is likely that the West will win the cold war",
                                               type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 6)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 6)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 6)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 6)

    create_question(db, schemas.QuestionCreate(text="I am a religious person",
                                               type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 7)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 7)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 7)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 7)

    create_question(db, schemas.QuestionCreate(text="Please describe your earliest memory in as much detail as possible",
                                               type="freeform", required = False))

    create_question(db, schemas.QuestionCreate(text="What did you experience about during your last dream?", type="freeform", required = False))

    create_question(db, schemas.QuestionCreate(text="My sexual relationships are satisfying",
                                               type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 10)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 10)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 10)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 10)

    create_question(db, schemas.QuestionCreate(text="A certain train is 125 m long. It passes a man, running at 5 km/hr in the same direction in which the train is going. It takes the train 10 seconds to cross the man completely. Then the speed of the train is: ",
                                               type="pickone", required=False))
    create_question_option(db, schemas.QuestionOptionCreate(value="60 km/h"), 11)
    create_question_option(db, schemas.QuestionOptionCreate(value="66 km/h"), 11)
    create_question_option(db, schemas.QuestionOptionCreate(value="50 km/h"), 11)
    create_question_option(db, schemas.QuestionOptionCreate(value="55 km/h"), 11)


    # Recipes messages
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="test", message="This is a", target_board = "recipes"), custom_time="1990-03-1 12:31")

