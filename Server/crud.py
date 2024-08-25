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


def add_answer(db: Session, answer: schemas.AnswerCreate):
    db_answer = models.Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def get_highest_submission_id(db: Session) -> int:
    highest_submission_id = db.query(func.max(models.Answer.submission_id)).scalar()
    if highest_submission_id is None:
        return 0  # If there are no submissions yet, start from 0 (or 1 if you prefer)
    return highest_submission_id


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
    db.query(models.ClubMembership).delete()
    db.query(models.NewsArticle).delete()
    db.commit()


def get_all_club_members_by_club(db: Session, club_name: str, run: int = 1):
    result = []
    if run == 1:
        club_members = db.query(models.ClubMembership).filter(models.ClubMembership.club_run_1 == club_name)
        for member in club_members:
            result.append(schemas.ClubMembership(first_name=member.first_name, last_name=member.last_name,
                                                 nickname=member.nickname, title=member.title_run_1))
    else:
        club_members = db.query(models.ClubMembership).filter(models.ClubMembership.club_run_2 == club_name)
        for member in club_members:
            result.append(schemas.ClubMembership(first_name=member.first_name, last_name=member.last_name,
                                                 nickname=member.nickname, title=member.title_run_1))

    return result


def check_author_username_password_valid(db: Session, username: str, password: str) -> bool:
    """
    Check if the username and password for an author are valid. Since we don't want actual security, we don't
    do any salting, hashing or any of that stuff.
    """
    author = db.query(models.Author).filter(models.Author.name == username).filter(models.Author.password == password).first()
    if author:
        return True

    return False


def create_club_membership(db: Session, first_name: str, last_name: str, nickname: str, club_run_1: str, club_run_2: str, title_run_1: str = "", title_run_2: str = ""):
    db_membership = models.ClubMembership(first_name=first_name, last_name=last_name, nickname=nickname, club_run_1=club_run_1, club_run_2=club_run_2, title_run_1=title_run_1, title_run_2=title_run_2)

    db.add(db_membership)
    db.commit()


def create_news_article_custom_time(db: Session, username, article_text, article_subject: str, time_to_use: str):
    author = db.query(models.Author).filter(models.Author.name == username).first()
    new_article = models.NewsArticle(title=article_subject, text=article_text, author_id=author.id, time=time_to_use)
    db.add(new_article)
    db.commit()


def create_news_article(db: Session, username: str, article_text: str, article_subject: str):
    time = datetime.now()
    time = time.replace(year=1991)
    time_to_use = time.strftime("%Y-%m-%d %H:%M")
    create_news_article_custom_time(db, username, article_text, article_subject, time_to_use)




def _seed_questions(db: Session):
    create_question(db, schemas.QuestionCreate(text="What is your age?", type="integer", required=True))
    create_question(db, schemas.QuestionCreate(text="What is your gender?", type="pickone", required=True))
    create_question(db,
                    schemas.QuestionCreate(text="What type of profession do you have?", type="pickone", required=True))
    create_question(db, schemas.QuestionCreate(text="What is your relationship status?", type="pickone", required=True))


    create_question(db, schemas.QuestionCreate(text="What is your starsignt?", type="pickone", required=True))


    # Gender
    create_question_option(db, schemas.QuestionOptionCreate(value="Male"), 2)
    create_question_option(db, schemas.QuestionOptionCreate(value="Female"), 2)

    # Profession
    create_question_option(db, schemas.QuestionOptionCreate(value="Professional"), 3)
    create_question_option(db, schemas.QuestionOptionCreate(value="Business owner"), 3)
    create_question_option(db, schemas.QuestionOptionCreate(value="Unemployed"), 3)
    create_question_option(db, schemas.QuestionOptionCreate(value="Public services"), 3)
    create_question_option(db, schemas.QuestionOptionCreate(value="Student"), 3)
    create_question_option(db, schemas.QuestionOptionCreate(value="Creative"), 3)

    # Marital status
    create_question_option(db, schemas.QuestionOptionCreate(value="Single"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Engaged"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Married"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Widowed"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Divorced"), 4)
    create_question_option(db, schemas.QuestionOptionCreate(value="Separated"), 4)

    # Starsign
    create_question_option(db, schemas.QuestionOptionCreate(value="Aries"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Taurus"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Gemini"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Cancer"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Leo"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Virgo"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Libra"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Scorpio"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Sagittarius"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Capricorn"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Aquarius"), 5)
    create_question_option(db, schemas.QuestionOptionCreate(value="Pisces"), 5)

    '''# Add some of the not required questions
    create_question(db, schemas.QuestionCreate(text="It is impossible to stay faithful to one’s spouse for 40 years", type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 6)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 6)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 6)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 6)

    create_question(db, schemas.QuestionCreate(text="It is likely that the West will win the cold war",
                                               type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 7)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 7)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 7)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 7)

    create_question(db, schemas.QuestionCreate(text="I am a religious person",
                                               type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 8)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 8)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 8)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 8)

    create_question(db, schemas.QuestionCreate(text="Please describe your earliest memory in as much detail as possible",
                                               type="freeform", required = False))

    create_question(db, schemas.QuestionCreate(text="What did you experience about during your last dream?", type="freeform", required = False))

    create_question(db, schemas.QuestionCreate(text="My sexual relationships are satisfying",
                                               type="pickone", required = False))
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Disagree"), 11)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Disagree"), 11)
    create_question_option(db, schemas.QuestionOptionCreate(value="Slightly Agree"), 11)
    create_question_option(db, schemas.QuestionOptionCreate(value="Strongly Agree"), 11)

    create_question(db, schemas.QuestionCreate(text="A certain train is 125 m long. It passes a man, running at 5 km/hr in the same direction in which the train is going. It takes the train 10 seconds to cross the man completely. Then the speed of the train is: ",
                                               type="pickone", required=False))
    create_question_option(db, schemas.QuestionOptionCreate(value="60 km/h"), 12)
    create_question_option(db, schemas.QuestionOptionCreate(value="66 km/h"), 12)
    create_question_option(db, schemas.QuestionOptionCreate(value="50 km/h"), 12)
    create_question_option(db, schemas.QuestionOptionCreate(value="55 km/h"), 12)'''


def _seed_recipe_messages(db: Session):
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



def _seed_alien_messages(db):
    ####### ALIEN MESSAGES

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="John",
                                                                            message="I've always believed in the unexplained. Seeing this site gives me hope that we can uncover the truth about crop circles.",
                                                                            target_board="alien"),
                                         custom_time="1991-01-05 14:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Emily",
                                                                            message="I saw strange lights over a field last summer. It's a relief to find others who are curious about these phenomena. More people from the village saw them, but noone could tell us what we saw exactly. Some folks with governement credentials told us that it was just a weather baloon. But they don't give of light, do they?",
                                                                            target_board="alien"),
                                         custom_time="1991-01-12 09:15")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Mark",
                                                                            message="I've been fascinated by crop circles for years. Finally, a place to discuss and share theories!",
                                                                            target_board="alien"),
                                         custom_time="1991-02-01 11:20")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Sara",
                                                                            message="I found this site through a friend. The stories here are incredible. I no longer feel alone in my experiences.",
                                                                            target_board="alien"),
                                         custom_time="1991-02-15 16:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tom",
                                                                            message="Skeptics may say it's all fake, but the precision of these formations can't be ignored. Glad to see a community forming around this.",
                                                                            target_board="alien"),
                                         custom_time="1991-03-10 13:50")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Anna",
                                                                            message="I saw my first crop circle back in 1985. It's amazing to finally find others who are as intrigued as I am.",
                                                                            target_board="alien"),
                                         custom_time="1991-03-25 10:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Brian",
                                                                            message="This site is a beacon for those of us who seek the truth. Crop circles are just the beginning.",
                                                                            target_board="alien"),
                                         custom_time="1991-04-02 15:10")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Lara",
                                                                            message="Finding this community feels like coming home. I've had experiences I can't explain and now I can share them with others.",
                                                                            target_board="alien"),
                                         custom_time="1991-04-15 09:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="David",
                                                                            message="I've read about crop circles for years, but never had a place to discuss. This is fantastic!",
                                                                            target_board="alien"),
                                         custom_time="1991-05-01 17:25")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Ella",
                                                                            message="The energy at crop circle sites is palpable. I've visited quite a few of them. Every time I do I sleep better and feel refreshed for weeks. It works better for certain types than for others though. Does anyone know why?",
                                                                            target_board="alien"),
                                         custom_time="1991-05-10 08:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Frank",
                                                                            message="I used to think I was crazy for believing that crop circles are the work of actual aliens. This community is helping me realize I'm not alone.",
                                                                            target_board="alien"),
                                         custom_time="1991-05-20 14:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Grace",
                                                                            message="Just discovered this site. The testimonials here are powerful. I'm convinced there's more to crop circles than meets the eye.",
                                                                            target_board="alien"),
                                         custom_time="1991-06-01 12:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Henry",
                                                                            message="Grace, I feel the same way. This community is growing and so is our understanding of these phenomena.",
                                                                            target_board="alien"),
                                         custom_time="1991-06-15 16:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Isabel",
                                                                            message="I've always been fascinated by the unexplained. Finding this site has reignited my passion for the truth.",
                                                                            target_board="alien"),
                                         custom_time="1991-06-25 11:15")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Jack",
                                                                            message="Crop circles are just the tip of the iceberg. This community is a step towards uncovering greater mysteries.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-05 13:40")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Karen",
                                                                            message="I've witnessed a crop circle being formed by strange lights. It was one of the most magical experiences in my life. I never really told anyone about it as i was affraid that people would think i'm loonie if i told them about it. This is the first time that i dared even to say something about it. Whatever the aliens want, i'm a 100% sure that they are here to help us out even if we don't understand how or why!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-10 18:20")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Leo",
                                                                            message="Karen, your story is incredible. It's experiences like yours that make this community so important.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-12 14:50")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Mia",
                                                                            message="The stories here are amazing. I feel like I'm finally part of a community that understands.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-13 09:35")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Nathan",
                                                                            message="I've been searching for a place to share my experiences. This site is exactly what I've been looking for.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-15 15:05")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Olivia",
                                                                            message="Nathan, welcome! We're all here to uncover the truth together. Your experiences are valuable.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-16 10:25")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Peter",
                                                                            message="I've always been a skeptic, but the discussions here are making me question what I thought I knew.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-16 12:55")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Quinn",
                                                                            message="Peter, it's good to have skeptics too. It keeps the discussion balanced and grounded.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-17 11:10")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Rachel",
                                                                            message="I've experienced things I just can't explain away, as much as i want to (or ya know, probably should?). It's comforting to know I'm not alone in this.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-17 13:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Steve",
                                                                            message="This site has become my go-to place for all things unexplained. The community here is a-m-a-z-i-n-g.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-17 16:20")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tina",
                                                                            message="I never thought I'd find a community like this. The stories here are incredible and inspiring.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-18 14:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Uma",
                                                                            message="I've always felt a connection to the unexplained. This site is a treasure trove of information and experiences.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-18 15:50")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Victor",
                                                                            message="The discussions here are changing my perspective. Crop circles might be more than just hoaxes.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-18 17:40")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Wendy",
                                                                            message="Victor, I had my doubts too, but the evidence and testimonials here are compelling. You can't just dismiss all of these people as having hallucinations.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-19 13:20")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Xander",
                                                                            message="Wendy, the community here is great for keeping an open mind while seeking the truth.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-19 15:35")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Yvonne",
                                                                            message="I'm so glad I found this site. The stories and discussions are fascinating and eye-opening. I'm a big believer, but i never realized that the governement might have some vested interest in keeping it secret for us. I just thought that most people didn't care.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-20 11:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Zach",
                                                                            message="Yvonne, same here. This community is a great place to explore the mysteries of crop circles and beyond.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-20 14:25")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Alice",
                                                                            message="I saw my first crop circle in 1990 and it was a life-changing experience. There is no doubt in my mind that they are made by extraterrestrials. Keep searching for the truth!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-21 14:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Bob",
                                                                            message="While crop circles are fascinating, I remain skeptical. It seems more likely that they are human-made hoaxes rather than messages from aliens. Show me some real evidence!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-22 09:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Charlie",
                                                                            message="Bob, you should visit a crop circle in person. The energy and precision cannot be explained by human activity alone. I've felt the presence of something otherworldly!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-22 13:15")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Denise",
                                                                            message="I agree with Bob. It's too easy to jump to conclusions without solid proof. Let's keep an open mind but demand more evidence.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-23 10:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Erik",
                                                                            message="Denise and Bob, have you considered the historical context? Crop circles have been documented for centuries. They are not a modern phenomenon!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-23 15:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Faith",
                                                                            message="I recently witnessed strange lights over a field that later had a crop circle. It was incredible! We are not alone.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-23 20:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="George",
                                                                            message="Faith, what you saw could have been anything. Natural phenomena, experimental aircraft, who knows? Let's not rush to conclusions.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-24 07:20")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Hannah",
                                                                            message="George, your skepticism is healthy, but sometimes you have to trust your instincts. The truth is out there!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-24 18:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Ivan",
                                                                            message="I've been researching crop circles for years. The patterns often align with ancient sacred geometry. This can't be a coincidence.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-25 11:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Jane",
                                                                            message="Ivan, that's an interesting point. But couldn't it also be that humans are creating these patterns deliberately, inspired by ancient designs?",
                                                                            target_board="alien"),
                                         custom_time="1991-07-25 14:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Kate",
                                                                            message="Jane, why would people go to such lengths to create something so elaborate without taking credit? It doesn't make sense.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-25 17:15")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Jane",
                                                                            message="Kate, sometimes people do things for the thrill of it, or to perpetuate a mystery. We shouldn't discount human ingenuity.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-26 09:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Monica",
                                                                            message="I used to be a skeptic like Jame, but after seeing a crop circle myself, I can't deny the possibility of extraterrestrial involvement.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-26 19:45")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Nate",
                                                                            message="Hey Monica! What exactly changed your mind? Was it just the visual impact, or did you experience something more? My family is having a very hard time believing me and i've tried EVERYTHING. Me believing this is tearing us apart and it just hurts. So anything you can give me would help a lot!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 08:30")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Olivia",
                                                                            message="I had an eerie feeling of being watched while visiting a crop circle. It's not something I can easily explain, but it felt significant.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 15:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Jane",
                                                                            message="Olivia, feelings can be deceiving. Our brains are wired to find patterns and meaning, even where there may be none.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 16:20")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Quincy",
                                                                            message="The debate is what makes this topic so fascinating. Whether you believe or not, crop circles spark our curiosity and imagination. I for one don't really care if they are 'real' or not. Both situations make for an interesting story",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 18:50")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Rachel",
                                                                            message="Well said, Quincy. Let's keep discussing and exploring. The search for truth is a journey, not a destination.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 19:15")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Sam",
                                                                            message="I think it's important to approach this with scientific rigor. While the idea of extraterrestrial involvement is intriguing, we need to thoroughly investigate all possibilities. The assumption that it's aliens simply violates occam's razor!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 20:00")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tina",
                                                                            message="I agree that science is crucial, but sometimes science can't explain everything. There's a mystery here that goes beyond our current understanding. So all this talk about scientific 'rigor' is all nice and well, but we can't summon the circles. If we could, we might consider to put science to work on it. Now we just have to believe and experience what we feel!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 20:10")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Uma",
                                                                            message="I have been studying crop circles for over a decade, and there are too many anomalies that science cannot explain away as hoaxes or natural phenomena. That doesn't stop the non believers from trying though. But you can just use their own principles against them. If it really was people doing it, they would be able to explain all the stuff, right?!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 20:11")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Victor",
                                                                            message="Uma, what kind of anomalies are you referring to? Can you provide specific examples? When you say anomalies, i think about stuff like gravity not working right, time going backwards, that kind of stuff. We would have hard about that on the news if they found that right? I doubt any governement agency could keep that under wraps...",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 20:18")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Uma",
                                                                            message="For instance, I visited a crop circle last year, and the electromagnetic readings were off the charts. This isn't something that can be easily faked! That's not the work of some jokers pulling a prank.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 20:34")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Xander",
                                                                            message="Uma, those readings could have been affected by various factors. We need to be careful not to jump to conclusions based on anomalies.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 21:10")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Yvonne",
                                                                            message="I believe that crop circles are messages from other beings. The complexity and beauty of the designs are beyond human capability.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 21:35")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Zach",
                                                                            message="Yvonne, I think you're underestimating human creativity and overestimating the unknown. It's exciting, but we need to stay grounded.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 21:48")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Nathan",
                                                                            message="I'm so glad to see more people joining this discussion. It seems like every day, new evidence comes to light that makes it harder to dismiss crop circles as mere hoaxes. I remember the first time I saw one, back in the summer of '89. The air was electric, and there was this strange hum that I could feel more than hear. It's something that has stayed with me ever since.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 21:53")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Lara",
                                                                            message="Nathan, your story gives me chills. I've never experienced a crop circle firsthand, but I hope to one day. The more I read, the more convinced I become that there's a deeper meaning to these formations. Has anyone else felt that hum Nathan mentioned?",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 22:01")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Mia",
                                                                            message="Lara, I've felt something similar. When I visited a crop circle last year, there was this overwhelming sense of calm and an almost imperceptible vibration in the air. It was as if the circle itself was alive.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 22:24")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tom",
                                                                            message="It's fascinating to hear about these experiences. I've always approached crop circles with skepticism, but the personal accounts here are making me reconsider. Maybe it's time I visited one myself and saw what all the fuss is about.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 23:09")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Sara",
                                                                            message="Tom, you definitely should! Seeing a crop circle in person is a totally different experience from just reading about it. The scale, the detail, and the feeling you get standing in the middle of one... it's indescribable.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 23:46")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Frank",
                                                                            message="I've been visiting crop circles for over a decade, and each one is unique. Some seem simple, while others are incredibly intricate. I've always wondered if there's a message we're supposed to decode. Maybe if we all put our heads together, we can figure it out.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-27 23:59")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Emily",
                                                                            message="Frank, that's a great idea. I think there's definitely a pattern or a message in these formations. Has anyone here tried to decode them? What if we're missing something obvious?",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 00:03")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Brian",
                                                                            message="Emily, I've been trying to decode crop circles for years. Some believe they're maps, others think they're messages. I've even heard theories that they're musical notes. It's so intriguing to consider all the possibilities.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 00:12")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Alice",
                                                                            message="Brian, the idea of crop circles being musical notes is fascinating. I never thought of that! Maybe they're trying to communicate through a universal language that we haven't deciphered yet.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 00:49")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="John",
                                                                            message="Alice, that makes a lot of sense. Music is something that transcends cultures and even species. Perhaps the crop circles are a way to establish a common ground with us.",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 01:06")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Peter",
                                                                            message="I'm still on the fence about all this, but the idea of crop circles being a form of communication is intriguing. Has anyone tried to play the patterns like a musical score? What if that's the key to understanding them?",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 01:32")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tina",
                                                                            message="Sound? Music? How the hell would you even convert the circles into that? I'm sorry, i don't think it's music. I'm having a hard time believing that the visitors would hop into their UFO, travel lightyears to get here only so they can drop their latest and hottest mixtape with us? If you are right, it could be groundbreaking. But i for one am not getting my hopes up!",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 01:57")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Grace",
                                                                            message="I've always felt that crop circles had a deeper meaning. The idea that they could be music or some form of universal language resonates with me. Let's explore this further! What can we do to help? How could we even translate it?",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 01:58")

    create_guestbook_message_custom_time(db, schemas.GuestbookMessageCreate(author_name="Tom",
                                                                            message="I've been following this discussion closely, and I have to say, it's the most exciting theory I've heard in a long time. I'll try to find someone who can help us translate these patterns somehow. But keep in mind that we might be barking up the wrong tree...",
                                                                            target_board="alien"),
                                         custom_time="1991-07-28 06:30")


def _seed_news_articles(db):
    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Tensions flared at last night’s Parish Council meeting when local resident <strong>Hykka Jelbert</strong> was arrested after a violent altercation with <strong>Dr. Oscar Fitzwilliam</strong>. The incident occurred during a heated discussion about the memorial to the mine workers in the village square. Witnesses reported that the argument quickly escalated, leading to Hykka punching Dr. Fitzwilliam in the face, fracturing his jaw. Police were called to the scene, and Hykka was taken into custody shortly thereafter. This shocking event has left the village in disbelief, especially given the longstanding tensions related to the mine’s closure. Dr. Fitzwilliam is recovering, and Hykka now faces serious legal consequences for the assault.</p>",
                                    article_subject="Hykka Jelbert Arrested for Assaulting Dr. Oscar Fitzwilliam",
                                    time_to_use="1989-09-15 10:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Local hero alert! <strong>Jorun Nilsen</strong>, our very own fisherman, saved the day (and a dolphin!) near Whisper Bay's coastline. Spotting the poor creature struggling in shallow waters, Jorun didn’t hesitate for a second. He quickly jumped into action, guiding the dolphin back to safety with his boat. It took a few tense hours, but thanks to his quick thinking, the dolphin swam off into deeper waters, safe and sound. This has everyone talking about how we need to do more to protect our local wildlife. Some folks are even suggesting we should get some proper training and resources for situations like this. Hats off to Jorun!</p>",
                                    article_subject="Local Fisherman Saves Stranded Dolphin!",
                                    time_to_use="1990-06-12 14:30")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Whisper Bay has been rocked by the mysterious disappearance of <strong>Silla Chenoweth</strong>, the owner and managing director of the local tin mine. Silla was last seen preparing for a boating trip, but her boat was found adrift, with no sign of her. The mine, which has been the backbone of the local economy, has now been forced to close, leaving many villagers without work. The community is in shock, and the authorities are investigating, but so far, there are no leads. The village is holding its breath as we wait for any news on Silla’s whereabouts.</p>",
                                    article_subject="Mystery Surrounds Silla Chenoweth's Disappearance and Mine Closure",
                                    time_to_use="1990-09-15 08:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>There’s been a lot of talk about the <strong>Children of the Sacred Green</strong> lately, especially after their sudden decision to adopt celibacy as part of their doctrine. The spiritual commune, which has been part of Whisper Bay for a few years now, has always been a bit of a mystery to the locals. But this new development has some villagers feeling uneasy. Some are supportive, saying it’s just part of their spiritual journey, while others are worried about what this means for the future of the group. The tension is palpable, and only time will tell how this will play out.</p>",
                                    article_subject="Children of the Sacred Green Adopt Celibacy, Stirring Village Concerns",
                                    time_to_use="1991-02-15 15:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Dr. <strong>Oscar Fitzwilliam</strong> has returned to Whisper Bay after many years away, following his recent divorce. Oscar, once a beloved figure in the village, has taken up residence in his old family home. His return has sparked a lot of interest, especially among those who remember his high school romance with Aswen Pengelly, now a married mother of two. While some are curious about why Oscar has come back now, others are simply happy to see a familiar face returning to the village. Only time will tell how his return will affect the close-knit community.</p>",
                                    article_subject="Dr. Oscar Fitzwilliam Returns to Whisper Bay After Divorce",
                                    time_to_use="1991-03-05 10:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Whisper Bay has become a hub of activity with the arrival of a team of archaeologists led by <strong>Dr. Thomas Hammond</strong>, an old friend of Merryn and Aswen Pengelly. The team is starting a dig near the old tin mine, and rumors are swirling about what they might find. Some locals are hoping for ancient artifacts that could shed light on the village’s past, while others are just excited to have something new happening. The dig is open to the public, so if you’re curious, feel free to stop by and see history being unearthed right before your eyes!</p>",
                                    article_subject="Archaeologists Begin Dig Near Whisper Bay",
                                    time_to_use="1991-04-10 09:00")


    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>In an unusual twist for our quiet village, a group calling themselves the <strong>Cosmic Truth Seekers</strong> has arrived in Whisper Bay. These self-proclaimed alien hunters have set up camp near the old quarry, claiming they’ve detected strange readings and unexplained phenomena in the area. Equipped with all sorts of gadgets, from cameras to what they say are ‘energy detectors,’ they’re here to investigate local reports of mysterious lights and odd occurrences. Whether you believe in little green men or not, their presence has certainly brought a buzz to the village!</p>",
                                    article_subject="Alien Hunters Descend on Whisper Bay",
                                    time_to_use="1991-05-18 14:30")


    create_news_article_custom_time(db, username="admin",
                                    article_text="<p><strong>Henry Kempthorne</strong> has big plans for Whisper Bay! The local landowner has announced his intention to develop a holiday park on the outskirts of the village. The project, which is still in its early stages, is expected to include cabins, a small lake, and a variety of recreational facilities. While Henry is confident that the park will bring much-needed tourism and revenue to the village, not everyone is on board. Some residents worry that it could change the character of Whisper Bay forever. Henry is currently meeting with investors and local officials to move the project forward, so stay tuned for updates on this potentially transformative development.</p>",
                                    article_subject="Henry Kempthorne Plans Holiday Park in Whisper Bay",
                                    time_to_use="1991-06-22 11:00")


    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>The Whisper Bay Women's Institute pulled off another fantastic bake-off this year, and it was all for a good cause! The event was buzzing with delicious smells and happy faces, as dozens of cakes and pastries were laid out for judging. The star of the show? <strong>Mrs. Gwendoline Thomas</strong>, who wowed everyone with her Victoria Sponge. She took home the top prize, and the bake-off managed to raise over £500 for the local school. That money’s going to be used to buy some much-needed science lab equipment, so a big thanks to everyone who participated and donated. Can’t wait for next year’s sweet showdown!</p>",
                                    article_subject="Sweet Success at Whisper Bay Bake-Off!",
                                    time_to_use="1990-07-20 10:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Security concerns have been on the rise at the GCHQ listening station in Whisper Bay. <strong>Ross Thomas</strong>, who manages day-to-day operations, has been under pressure as the station experiences a series of data breaches and unauthorized access attempts. The situation has some residents worried, especially in light of the recent strange occurrences in the village. Ross and his team are working hard to tighten security, but the source of these breaches remains a mystery. With so much going on, it’s no wonder that people are starting to ask questions about what exactly is happening behind those secure walls.</p>",
                                    article_subject="Security Issues Plague Whisper Bay Listening Station",
                                    time_to_use="1991-07-25 14:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>With the <strong>Harvest Fête</strong> just around the corner, the excitement in Whisper Bay is building up! This year’s fête is shaping up to be one of the biggest yet, and folks are saying it couldn’t come at a better time. After all the strange goings-on recently, the fête is a chance for everyone to come together and have some fun. Expect all the usual favorites—traditional games, a baking contest, and of course, the crowning of the <strong>Monarch of the Harvest</strong>. Local businesses are chipping in with prizes, and volunteers are working hard to make sure everything goes off without a hitch. It’s going to be a great day, so make sure to mark your calendars for September 15!</p>",
                                    article_subject="Whisper Bay Gears Up for the Harvest Fête!",
                                    time_to_use="1991-09-01 09:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Great news, everyone—<strong>Whiskers</strong> is home safe! Mrs. Blythe’s beloved tabby, who went missing for three whole days, has finally been found. Turns out, she was just taking an unexpected nap in Mr. Davies' garden shed. Mrs. Blythe has been beside herself with worry, so you can imagine her relief when Whiskers was finally returned home. The whole village came together to search for the little escape artist, and Mrs. Blythe is incredibly grateful to everyone who helped out. A big purr of thanks to all!</p>",
                                    article_subject="Whiskers the Cat Found Safe After Three Days!",
                                    time_to_use="1991-09-01 16:45")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Exciting news for all you theater lovers! <strong>John Smith</strong>, our local teacher and drama enthusiast, has announced that Whisper Bay will be putting on a production of Shakespeare's <em>A Midsummer Night's Dream</em>. Auditions are open to anyone brave enough to try their hand at acting, and John says there’s no experience required—just enthusiasm! Rehearsals will start next week, and the play is set to be performed in late October. It’s a great chance to get involved and show off your creative side. Plus, it’s sure to be a lot of fun!</p>",
                                    article_subject="Community Theater to Perform 'A Midsummer Night's Dream'",
                                    time_to_use="1991-09-03 11:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>We’ve had some shocking news here in Whisper Bay—a massive landslide hit on September 7, destroying several homes and cutting off phone lines and road access. It’s been a tough few days, but thankfully, there was only one casualty: <strong>Pascoe Roseveare</strong>, who’s now in a coma. The community is rallying to help those who lost their homes, with neighbors opening their doors and volunteers working non-stop. The cause of the landslide is still under investigation, but some folks are worried it might be linked to recent activities in the area. It’s a difficult time, but we’ll get through this together.</p>",
                                    article_subject="Catastrophic Landslide Strikes Whisper Bay",
                                    time_to_use="1991-09-07 18:15")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>In a heartwarming display of community spirit, the <strong>Kempthorne</strong> family has taken in the <strong>Pengelly</strong> family, who were left homeless after the recent landslide. The Kempthornes didn’t think twice about offering their home to the Pengellys during this difficult time. This is just one example of how folks in Whisper Bay are coming together to help each other out. The Pengellys have lost almost everything, but thanks to the Kempthornes’ generosity, they’ve found some stability amidst the chaos. As more families are rehoused and life slowly returns to normal, it’s clear that Whisper Bay’s community spirit is stronger than ever.</p>",
                                    article_subject="Kempthornes Welcome Pengellys After Landslide",
                                    time_to_use="1991-09-08 10:30")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>In a bit of good news, <strong>Spot</strong>, the Davies family’s charming Dalmatian, took home the top prize at this year’s Whisper Bay Dog Show! Spot wowed the judges and onlookers alike with his impeccable behavior and stylish spots, earning the coveted title of Best in Show. The event brought some much-needed joy to the village, especially after all the recent upheaval. Funds raised from the show will go toward repairing the roof of the village hall, so it was all for a good cause too. Congrats to Spot and the Davies family!</p>",
                                    article_subject="Spot Wins Best in Show at Whisper Bay Dog Show",
                                    time_to_use="1991-09-09 15:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>The village of Whisper Bay was struck with concern last night as local teenager <strong>Demelza Jelbert</strong> was rushed to the hospital after a sudden medical emergency. Sources say Demelza, known to many as 'Demi', was found unresponsive in her room, prompting immediate action from her family. While details remain sparse, and out of respect for her and her family’s privacy, it’s enough to say that the situation was serious. Fortunately, thanks to swift medical intervention, Demi is now stable and under observation at the hospital. The community has come together to offer support, with many expressing relief that she is on the road to recovery. We all hope to see Demi back in the village soon, healthy and surrounded by those who care about her.</p>",
                                    article_subject="Demelza Jelbert Hospitalized After Medical Emergency",
                                    time_to_use="1991-09-09 22:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>There’s been a bit of a stir in Whisper Bay lately—<strong>Mrs. Green’s</strong> prize-winning roses have gone missing! Sometime during the night of September 10, the beautiful blooms were stolen right out of her garden. Mrs. Green is heartbroken, and the whole village is buzzing with speculation about who could have taken them. These roses aren’t just any flowers—they’ve won awards and are the pride of Mrs. Green’s garden. If anyone has any information, they’re encouraged to come forward. Let’s help get those roses back where they belong!</p>",
                                    article_subject="Mystery in the Garden: Prize-Winning Roses Stolen!",
                                    time_to_use="1991-09-11 08:45")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>We’ve got a bit of a mystery on our hands—<strong>Hope Pengelly</strong>, a local teenager, has gone missing. She was last seen on September 12, and while at first, folks thought she might have just run off, the police are now taking things seriously. They’ve brought in some expert detectives to help with the search, and the whole village is on edge. If you’ve seen or heard anything, please reach out to the authorities. Everyone’s hoping for Hope’s safe return.</p>",
                                    article_subject="Local Teenager Hope Pengelly Missing",
                                    time_to_use="1991-09-12 13:15")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>Tensions are running high in Whisper Bay following a disturbing incident involving <strong>Aswen Pengelly</strong> and <strong>Felicity Kempthorne</strong>. According to witnesses, Aswen confronted Felicity yesterday, accusing her of hiding information about his missing daughter, <strong>Hope Pengelly</strong>. The confrontation quickly escalated, with Aswen reportedly becoming physically aggressive. <b>Dr. Oscar Fitzwilliam</b> was called to the scene and had to sedate Aswen, who was in a highly agitated state. The incident has left many in the community shaken, and questions about Hope’s disappearance are now more pressing than ever. Felicity has not commented on the incident, and the police are continuing their investigation. It’s a tense time for everyone in the village as we await more information.</p>",
                                    article_subject="Aswen Pengelly Assaults Felicity Kempthorne Amid Tensions Over Hope's Disappearance",
                                    time_to_use="1991-09-12 17:00")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>There’s nothing like a good picnic to lift everyone’s spirits, and that’s exactly what happened on September 13 when the Women’s Institute organized a spontaneous gathering on the village green. It was a lovely day filled with laughter, delicious homemade treats, and a much-needed break from the recent events that have shaken Whisper Bay. Sometimes, it’s the simple things that bring a community together, and this picnic was a perfect example of that.</p>",
                                    article_subject="Spontaneous Picnic Brings Joy to Village Green",
                                    time_to_use="1991-09-13 14:30")

    create_news_article_custom_time(db, username="admin",
                                    article_text="<p>The final preparations are underway for the <strong>Harvest Fête</strong>, and Whisper Bay is buzzing with anticipation! Volunteers have been working tirelessly to ensure that everything is ready for the big day, and it’s looking like this year’s fête will be one to remember. Despite everything that’s been happening lately, the fête is a chance for the community to come together, have some fun, and celebrate the harvest season. There will be games, contests, and of course, the crowning of the Monarch of the Harvest. Don’t miss it!</p>",
                                    article_subject="Harvest Fête Preparations Near Completion",
                                    time_to_use="1991-09-14 12:00")



def seed_database(db: Session):
    # Add the default stuff in the datbase

    _seed_questions(db)
    _seed_recipe_messages(db)
    _seed_alien_messages(db)

    # Authors
    create_author(db, "Jaime", "Test")

    create_author(db, "admin", "somepassword")
    _seed_news_articles(db)




    # TEST USER
    create_club_membership(db, "Jaime", "van Kessel", "Nallath", club_run_1="FrivolousEngineering", club_run_2="FrivolousEngineering", title_run_1="Chief untouchable engineering", title_run_2="Chief untouchable engineering")
    create_club_membership(db, "Corne", "van Kessel", "BlazingEclipse", club_run_1="FrivolousEngineering", club_run_2="FrivolousEngineering", title_run_1="Chief touchable Engineering", title_run_2="Chief touchable Engineering")
    # Left title empty on purpose for testing purposes
    create_club_membership(db, "Roos", "Schultheiss", "Fjadderal", club_run_1="FrivolousEngineering", club_run_2="FrivolousEngineering", title_run_1="", title_run_2="")

    create_club_membership(db, "Felicity", "Kempthorne", "", club_run_1="wi", club_run_2="wi", title_run_1="Chairwomen", title_run_2="Chairwomen")

    create_club_membership(db, "Rosenwyn", "Jelbert", "Roz", club_run_1="wi", club_run_2="wi")
