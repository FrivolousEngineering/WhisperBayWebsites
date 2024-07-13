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


def get_authors(db: Session):
    return db.query(models.Author)


def get_news_articles(db: Session):
    return db.query(models.NewsArticle).order_by(models.NewsArticle.id.desc())

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


def update_option_text(db: Session, option_id: int, new_text: str):
    db_question_option = get_question_option(db, option_id)
    db_question_option.value = new_text
    db.commit()


def create_author(db: Session, name, password):
    db_author = models.Author(name=name, password = password)
    db.add(db_author)
    db.commit()


def reset_database(db: Session):
    db.query(models.Answer).delete()
    db.query(models.Question).delete()
    db.query(models.QuestionOption).delete()
    db.query(models.GuestbookMessage).delete()
    db.commit()


def check_author_username_password_valid(db: Session, username: str, password: str) -> bool:
    """
    Check if the username and password for an author are valid. Since we don't want actual security, we don't
    do any salting, hashing or any of that stuff.
    """
    author = db.query(models.Author).filter(models.Author.name == username).filter(models.Author.password == password).first()
    if author:
        return True

    return False


def create_news_article(db: Session, username: str, article_text: str, article_subject: str):
    author = db.query(models.Author).filter(models.Author.name == username).first()
    time = datetime.now()
    time = time.replace(year=1991)
    time_to_use = time.strftime("%Y-%m-%d %H:%M")
    new_article = models.NewsArticle(title = article_subject, text = article_text, author_id = author.id, time = time_to_use)
    db.add(new_article)
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
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="John Smith",
                                                                            message="Absolutely loved the recipe for Cornish pasties! Reminds me of my grandmother's cooking. Keep up the great work!",
                                                                            target_board="recipes"),
                                         custom_time="1991-01-12 14:30")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Mary Parker",
                                                                            message="Thank you for the wonderful saffron cake recipe. I tried it yesterday, and my family couldn't get enough. Can't wait to try more!",
                                                                            target_board="recipes"),
                                         custom_time="1991-01-18 09:45")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="David Lee",
                                                                            message="Fantastic collection of recipes! The recipes were a hit at our last family gathering. Do you have any recipes for traditional Cornish fish dishes?",
                                                                            target_board="recipes"),
                                         custom_time="1991-02-02 17:10")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Sue Wilson",
                                                                            message="This site is a treasure trove of Cornish culinary delights. The cake recipe is spot on. Cheers!",
                                                                            target_board="recipes"),
                                         custom_time="1991-02-14 12:20")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tom Roberts",
                                                                            message="Thanks for sharing these recipes. The Cornish pasties took me back to my childhood. Looking forward to more authentic Cornish recipes.",
                                                                            target_board="recipes"),
                                         custom_time="1991-03-01 08:35")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Helen White",
                                                                            message="Just tried the figgy 'obbin recipe - delicious! This site is now my go-to for all things Cornish. Keep adding more recipes!",
                                                                            target_board="recipes"),
                                         custom_time="1991-03-12 10:50")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Paul Brown",
                                                                            message="I had some issues reading your website? Would it be possible to make things a bit more readable? Selecting the text helped enough, but it would be nice if we could do without. Loved the recipes though!",
                                                                            target_board="recipes"),
                                         custom_time="1991-03-29 15:25")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Annette Green",
                                                                            message="Wonderful site with authentic Cornish recipes. The clotted cream recipe was divine. Any tips on making it extra thick?",
                                                                            target_board="recipes"),
                                         custom_time="1991-04-08 11:00")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Rob Harris",
                                                                            message="Thank you for the Cornish pasty recipe. It brought back so many memories. Do you have any vegan alternatives?",
                                                                            target_board="recipes"),
                                         custom_time="1991-04-20 13:40")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Liz Miller",
                                                                            message="UGH! What is up with the creepy fish pie?! Do people in the UK really eat that?! It looks freaking disgusting!",
                                                                            target_board="recipes"),
                                         custom_time="1991-05-05 16:55")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Geoff Walker",
                                                                            message="Just ignore the hatefull comment from Liz. I've been searching for a good recipe for Cornish Stargazy Pie, and yours was perfect. Thank you for preserving our heritage!",
                                                                            target_board="recipes"),
                                         custom_time="1991-05-18 07:15")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Emily Clark",
                                                                            message="Your Cornish cream guide was fantastic. My friends loved it. Please post more traditional dessert recipes!",
                                                                            target_board="recipes"),
                                         custom_time="1991-06-03 14:50")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Nigel Hall",
                                                                            message="Finally, a site dedicated to Cornish food! The recipes are authentic and easy to follow. Great job!",
                                                                            target_board="recipes"),
                                         custom_time="1991-06-18 09:05")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Margaret Adams",
                                                                            message="Tried the Cornish under roast recipe. It was a hit at our Sunday dinner. Your website is a wonderful resource.",
                                                                            target_board="recipes"),
                                         custom_time="1991-07-01 10:30")
    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Chris Davis",
                                                                            message="Love the attention to detail in your recipes. The Cornish pasties were just like my mum used to make. Thank you!",
                                                                            target_board="recipes"),
                                         custom_time="1991-07-20 17:20")


    # Authors
    create_author(db, "Jaime", "Test")
