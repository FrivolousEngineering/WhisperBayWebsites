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
    db.query(models.Prediction).delete()
    db.commit()


def create_prediction(db: Session, name: str, text_1: str, text_2: str, text_3: str):
    first_name = name.split(" ")[0]
    db_prediction = models.Prediction(first_name=first_name, severity=0, text = text_1)
    db.add(db_prediction)
    db_prediction = models.Prediction(first_name=first_name, severity=1, text=text_2)
    db.add(db_prediction)
    db_prediction = models.Prediction(first_name=first_name, severity=2, text=text_3)
    db.add(db_prediction)
    db.commit()


def find_prediction(db: Session, first_name: str):
    escalation_level = db.query(models.RunState).first().escalation_level

    result = db.query(models.Prediction).where((models.Prediction.first_name == first_name) & (models.Prediction.severity == escalation_level)).first()
    if result:
        return result.text
    return ""



def _seed_predictions(db: Session):
    create_prediction(db, "Aswen Pengelly",
                      "Nurture your mental health; it’s just as important as your physical well-being.",
                      "Hold on to the present moment. The decisions you make in the here and now will decide your future so stop worrying about the past.",
                      "She’s gone. Accept it and move on with your life… or maybe you could join her.")
    create_prediction(db, "Merryn Pengelly", "Persistence is your greatest weapon; use it wisely.",
                      "Don’t let family issues stand in the way of your self-realisation. You are a born hero so act on your instincts.",
                      "Maybe you could still save her, but becoming a real hero now seems a big stretch. Accept your shortcomings and failures and move on.")
    create_prediction(db, "Benesek Tredinnick",
                      "Pursue your passions with dedication, but remember to balance work with time for yourself and loved ones. Tradition is important, but don’t let it stifle innovation.",
                      "You will experience setbacks in your quest. Don't let them discourage you, but be aware of the sacrifices you'll have to make.",
                      "Give up on your pointless crusade and focus on protecting your family. You can never hope to win - I am stronger than you.")
    create_prediction(db, "Enigoe Tredinnick",
                      "Embrace your heritage, but don’t let the weight of the past crush your spirit—forge your own path.",
                      "Lightheartedness is important, but so is knowing when to be serious. Don't drift apart from those who really matter.",
                      "You’ll never live up to your family’s legacy, but you know that already. The shadows you fight are too strong—just give up now.")
    create_prediction(db, "Rosenwyn Jelbert",
                      "Loyalty is a beautiful trait, but remember to stay true to yourself above all else.",
                      "Life is not always a comedy - someone dies, and suddenly it's a tragedy instead. Be ready for things to change soon.",
                      "Your loyalty will get you nowhere. The people you trust will betray you—stop wasting your time, focus on yourself instead.")
    create_prediction(db, "Gwynnever Roseveare",
                      "Trust your instincts, and don't be afraid to carve your own path—your voice matters, and it's powerful.",
                      "New love is beautiful, but can be dangerous, too. Don't forget about past loves and their impact on your life.",
                      "They will find out and they will punish you for it, in ways you don't expect. Abandon all hope. You cannot hide.")
    create_prediction(db, "Locryn Chenoweth", "Business is important, but so is community—find the balance.",
                      "Secrets have a way of always coming out, and if you let them fester, they turn into an ugly thing. Let them out, or kill them for good.",
                      "Stop clinging to things you can no longer have - the past is the past, you can't trap it. In the end, you will be alone, and nothing will be perfect.")
    create_prediction(db, "Oscar Fitzwilliam", "Healing others is noble, but don’t forget to take care of yourself.",
                      "Death is just another part of life. But life has value and should be embraced - don't be too eager for the final act.",
                      "Death and decay will be with you forevermore, and will be all you'll ever know. There is no room for love when you've embraced Decay.")
    create_prediction(db, "Sevi Jelbert", "Loyalty is admirable, but don’t let it cloud your judgement.",
                      "The spirits have protected you always, but beware - some day soon they might turn away and allow the shadows in.",
                      "Your loyalty is your downfall. No one’s worth the sacrifices you’ve made.")
    create_prediction(db, "Tegen Chenoweth",
                      "Seek out mentors who can guide and support you; their wisdom is invaluable.",
                      "Curiosity is valuable, but be careful where it leads you.",
                      "Your Harvest dream is over and done. Mediocrity is all you can expect from life from here on out. Your only chance of being something greater is by going with them.")
    create_prediction(db, "Caradoc Grose",
                      "Cultivate gratitude; appreciating what you have fosters a more content and joyful life.",
                      "Envy is an ugly beast, and what goes around comes around. Don't get caught in the jaws of karmic justice.",
                      "You are second best, in everything, always. Never the best. Accept that this is your life,give up your dreams, and try to find whatever peace you can in this miserable mortal coil.")
    create_prediction(db, "Demelza Jelbert",
                      "Surround yourself with people who uplift and inspire you; friendships are your strongest allies.",
                      "Hold on to those dear and close to your heart. Some friends are irreplaceable, and once they're gone, you won't be able to replace them.",
                      "You aren't loved in the way that you want to be. Accept this, and the pain will go away. If it doesn't - better luck next time. Hope awaits.")
    create_prediction(db, "Paul Smith",
                      "Take responsibility for your actions; accountability is a key aspect of maturity.",
                      "Your secrets are safe for now, but be prepared for the consequences.",
                      "Realise that all of this is your fault, and yours alone. You can't run and hide from the truth any longer.")
    create_prediction(db, "Faythely Pengelly", "Your journey isn’t over—keep searching for the truth.",
                      "Dreams are fragile. Be careful—they have a way of shattering when reality creeps in.",
                      "Who are you? Do you even know anymore? You're a dead girl. Embrace it.")
    create_prediction(db, "Wendy Kempthorne",
                      "Invest in your education and independence; the world is changing, and your future is in your hands.",
                      "The façade you’ve built is cracking. Sooner or later, the truth will slip through.",
                      "You think they care for you, but you are a means to an end for them. Nothing less, but nothing more.")
    create_prediction(db, "Noah Angwin",
                      "Remember, it's okay to say no—your time and energy are valuable, so protect them wisely.",
                      "Your mind is sharp, but sharp edges can cut. Watch out - you're not invincible.",
                      "You will never be more than you are now. Accept your life is a waste. You will never be good enough.")
    create_prediction(db, "Kenwyn Boscawen", "Past mistakes don’t define you, but they do shape your future.",
                      "Ideals are admirable, but they can lead you astray. Not everyone shares your vision—beware.",
                      "There will never be justice in the world, and the utopia you dream about is further from your reach than it ever was. You will be better off if you accept this.")
    create_prediction(db, "John Smith",
                      "Learn to communicate your needs clearly; effective communication is key in all relationships.",
                      "Appearances can be deceiving—stay true to yourself amidst the lies.",
                      "Everything good and bad must come to an end, and soon. You need to make a choice, or it will be made for you.")
    create_prediction(db, "Linda Smith",
                      "Take time to discover what truly makes you happy; it’s the foundation of a fulfilling life.",
                      "A smile can hide a thousand secrets; don’t let them consume you.",
                      "When everything you ever wanted seems within reach, it's time to realise that you haven't wanted it for a long time. Embrace the hand you have been dealt.")
    create_prediction(db, "Henry Kempthorne",
                      "Learn to listen as much as you speak; true strength lies in understanding and empathy.",
                      "Ambition is a double-edged sword. The higher you climb, the further you have to fall.",
                      "Your legacy is a farce. It’s time to let go and disappear.")
    create_prediction(db, "Ursilla Chenoweth",
                      "Appearances can be deceiving, and disappearances are never simple—find the truth before it finds you.",
                      "You can change your name, but not your fate. It’s catching up with you—run while you can.",
                      "You’re better off lost. Stay hidden—it’s safer that way.")
    create_prediction(db, "Yannick Berkowitz", "The past doesn’t have to dictate your future—change is within reach.",
                      "The Angels have overlooked your failings until now and given you another chance. But judgement is coming for you.",
                      "You’re doomed to repeat your past. No one can escape their nature—not even you.")
    create_prediction(db, "Veronica Kempthorne", "Power isn’t everything—know when to step back.",
                      "Power slips through your fingers like sand. Hold on too tight, and you’ll lose it all.",
                      "Give up. Your time is over. It is my turn to take the reins.")
    create_prediction(db, "Zachary Angwin", "You’re stronger than you realize; don’t let others underestimate you.",
                      "You’re walking a fine line. One misstep, and you’ll find yourself on the wrong side.",
                      "Run away, you don't have a place here. You don't belong anymore, and you never will again. Just run away.")
    create_prediction(db, "Iger Moon", "Trust in the old ways, but don’t let tradition blind you to new possibilities.",
                      "The old gods are silent. Perhaps it’s time to listen to the whispers of doubt in your own mind.",
                      "The gods have abandoned you—your rituals are meaningless. It’s time to accept the truth and walk away.")
    create_prediction(db, "Xenara Moon",
                      "Your faith is strong, but remember that disappointment can lead to enlightenment.",
                      "Faith is fragile. It only takes a small crack to shatter it completely.",
                      "The stars say that you haven't been enough for a long time. You will not achieve your noble goal. Succumb to your base desires to make it all more bearable.")
    create_prediction(db, "Josep Boscawen", "Balance your past with your future; you have more control than you think.",
                      "Destiny calls, but it’s not the kind of call you can ignore. Answer carefully—it may not be what you hoped for.",
                      "Soon, everyone will realise that you are a fraud and a disappointment. Brace yourself for losing your chosen and real family.")
    create_prediction(db, "Davydh Roseveare",
                      "Remember that failure is not the end; it’s a stepping stone to your next success.",
                      "Keep your secrets close; not everyone is ready to hear them.",
                      "Your efforts will come to fruition eventually, but you will not be rewarded in the way you expect. You will be punished instead for all you have done.")
    create_prediction(db, "Anneth Enys", "You are a vessel, but don’t forget your own identity in the process.",
                      "The past is a heavy burden. It will weigh you down until you can no longer move forward.",
                      "Perhaps things would have been different if you hadn't been a failure. Soon, your insignificance will be truly revealed.")
    create_prediction(db, "Stefan Roseveare", "Sometimes, the quiet observer learns more than the loud leader.",
                      "You’re too weak to make a difference—just fade into the background where you belong.",
                      "You will serve no one, and save no one. Everything you're doing is inconsequential.")
    create_prediction(db, "Felicity Kempthorne", "Authority requires balance—lead with both your head and heart.",
                      "Control is an illusion. The tighter you grip it, the more it slips away.",
                      "You’re not as strong as you think. The station is doomed, and so are you.")
    create_prediction(db, "Georgina Czerny", "Your kindness is your strength—don’t let the world harden your heart.",
                      "Kindness can be a weakness. Be careful—it’s easy to be taken advantage of in a world like this.",
                      "The secrets you keep will destroy you. Your kindness will be your downfall. Abandon your post before it’s too late.")
    create_prediction(db, "Ross Thomas", "Trust no one, not even those closest to you.",
                      "Trust is dangerous - choose wisely who you give it to. In a place like this, betrayal lurks around every corner.",
                      "You’re not a hero, just a cog in the machine. Stop pretending you can make a difference.")
    create_prediction(db, "Tressa Moon",
                      "Take risks and step out of your comfort zone; that’s where real growth happens.",
                      "The things you hear aren’t always what they seem. Be cautious—some truths are best left unheard.",
                      "The knight in shining armor is usually nothing but a dream. Time to wake up, little light. Reality is calling.")
    create_prediction(db, "Philippa Tredinnick",
                      "Your curiosity is a gift, but tread carefully; not all secrets are meant to be uncovered.",
                      "Your curiosity will lead you somewhere dark. Be careful - some doors are better left unopened.",
                      "The girl with no past can't possibly have a future. And if the past can't be recovered, one should give up on the future.")
    create_prediction(db, "Lowen Grose",
                      "Stay grounded in your beliefs, but don’t be afraid to adapt when the winds of change blow.",
                      "Precision is your strength, but don’t let it blind you. Sometimes, the bigger picture is what matters most.",
                      "Your meticulous work won’t save you. The chaos is too great, and it’s only a matter of time before it swallows everything whole.")
    create_prediction(db, "Blake Fitzwilliam",
                      "Curiosity may have led you here, but it’s caution that will keep you safe.",
                      "The truth is out there, but finding it might cost you more than you’re willing to pay.",
                      "The truth isn’t out there. Stop searching before it drives you mad.")
    create_prediction(db, "Oliver Moon", "Wrath is a dangerous companion—keep it in check.",
                      "The past doesn’t forgive. You can’t escape it—sooner or later, it’ll find you.",
                      "Wrath. Wrath. Wrath. You will never escape the Wrath. Violence and rage is all there is and ever will be.")
    create_prediction(db, "Nathan Foxton", "Voices can guide, but not walk the path for you. Trust your own judgement.",
                      "Voices can be deceiving. Be careful which ones you listen to—they might not be who you think they are.",
                      "The voices will soon ring out no longer. They will turn away from you, and look for something else on a new world.")
    create_prediction(db, "Eric McCormick", "Sometimes, the truth is out there—but it’s not always what you expect.",
                      "The future isn’t as bright as you think. Darkness is coming—prepare yourself.",
                      "And from the darkness between the stars, He proclaimed: You're nothing, and will go down with everyone else.")
    create_prediction(db, "Hedra Tredinnick",
                      "Strength isn’t just physical—sometimes, the hardest battles are internal.",
                      "Justice is a slippery thing. You might find that what you’re seeking isn’t what you expected.",
                      "Find a new career path. You have no hope of protecting anything or anyone. Focus on simpler things which are in your capability.")
    create_prediction(db, "Chessen Angwin", "The law is clear, but justice isn’t always black and white.",
                      "The law is a heavy burden. Sometimes, it's better to let things go.",
                      "The law is broken, just like you. Stop pretending you can enforce it.")
    create_prediction(db, "Willym Enys", "The past holds many answers—don’t be afraid to dig deep.",
                      "The deeper you dig, the darker it gets. Some things are better left buried.",
                      "History is repeating itself. You’ll never uncover the truth—stop trying.")
    create_prediction(db, "Androw Redruth",
                      "The past is a lesson, not a life sentence—learn from it, but don’t let it define you.",
                      "Loyalty is a dangerous thing. It’s easy to lose yourself in it.",
                      "No matter what you do, everything will fall apart in the end. You’re just delaying the inevitable.")
    create_prediction(db, "Dorian Carter",
                      "The truth is your mission, but don’t forget to take care of the person searching for it.",
                      "The truth is elusive. Be careful—chasing it might lead you somewhere you don’t want to go.",
                      "You’re not the detective you think you are. The truth is out of your reach—stop trying to solve the unsolvable.")
    create_prediction(db, "Freya Mully",
                      "Tenacity is admirable, but know when to step back—sometimes, the answers come in the quiet moments.",
                      "Persistence is a virtue, but it can also be a curse. You need to let go sometimes.",
                      "All your hard work will amount to nothing. You’ll never get the recognition you crave—quit while you’re ahead.")
    create_prediction(db, "Thomas Hammond", "Knowledge is power, but only if it’s shared wisely.",
                      "Science can't explain everything. Some mysteries are better left unsolved.",
                      "The past is better left buried. Your dig is a waste of time.")
    create_prediction(db, "Selina Blair", "Knowledge is power, but power can be dangerous if misused.",
                      "Knowledge is power, but it’s also a burden. Be careful—it might be more than you can handle.",
                      "Your mission is a failure. You’re too late—let someone else clean up the mess.")
    create_prediction(db, "Maren Nilsen", "The earth holds many secrets—dig carefully.",
                      "The bones don't always hold the truth. Don't forget to make your own judgement - trust only bones, and you might find only death.",
                      "The earth holds no answers for you. Your work is futile—stop digging.")
    create_prediction(db, "Isette Redruth", "Your instincts are sharp—trust them, but don’t let them lead you astray.",
                      "Protection comes at a cost. Be prepared to pay it - nothing is ever truly safe.",
                      "Protection is a fantasy. You can’t save the village from itself.")
    create_prediction(db, "Ales Thomas", "Control is an illusion—learn to adapt when things fall apart.",
                      "Control is slipping. No matter how tightly you hold the reins, everything is bound to fall apart.",
                      "Your empire is crumbling. Accept that it’s over before it all comes crashing down.")
    create_prediction(db, "Hykka Jelbert", "Redemption is possible, but only if you truly desire it.",
                      "Redemption is slipping out of reach. The shadows of your past will never let you go.",
                      "You’re broken beyond repair. Stop pretending you have anything left to offer.")
    create_prediction(db, "Newlyn Noo Czerny", "The past haunts you, but it’s your future that needs your attention.",
                      "Run faster and further. The things that haunt you are right behind you.",
                      "You’ll never escape your demons. Give in—they’ve already won.")
    create_prediction(db, "Jorun Nilsen",
                      "Remember that sometimes the greatest gift you can give to a loved one is emotional openness. Different people have different languages of love. Beware stormy weather next Tuesday.",
                      "Stay true to your course, even when the waters get rough.",
                      "The sea won’t save you. Stop running and face the inevitable.")
    create_prediction(db, "Victor Czerny", "Science and the supernatural aren’t always at odds—find the balance.",
                      "Logic can only take you so far - some things can't be explained.",
                      "Science won’t save you from the supernatural. You’re chasing ghosts—give up.")
    create_prediction(db, "Remi Grigorio", "Be cautious of what you seek—it might just find you first.",
                      "Deception is a dangerous game. Sooner or later, the mask will slip.",
                      "You’ll never find what you’re looking for. The answers don’t exist—walk away.")
    create_prediction(db, "Kate Astell", "-", "-", "-")
    create_prediction(db, "Greg Borromead", "Trust your instincts; they can lead you to unexpected opportunities.",
                      "Your expertise is valuable, but in the wrong hands, it could be your undoing.",
                      "All your efforts are for nothing. The world is crumbling around you, and there’s no way to stop it.")
    create_prediction(db, "Fenella Borromead",
                      "Believe in your dreams, even when they seem far-fetched; persistence is key.",
                      "Your search for answers is admirable, but some questions should never be asked.",
                      "Did you want me to tell you that you are special and deserve a great life? You know the truth. You aren't, and you don't. Accept your failure and stay here, were you belong, in obscurity and insignificance.")



def update_escalation_state(db: Session, new_escalation_state: int):
    # Change the escalation state
    db_state = db.query(models.RunState).first()
    db_state.escalation_level =  new_escalation_state
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


    create_question(db, schemas.QuestionCreate(text="What is your starsign?", type="pickone", required=True))


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


def _seed_club_memberships(db):
    create_club_membership(db, "Aswen", "Pengelly", "", club_run_1="bowls", club_run_2="bowls")
    create_club_membership(db, "Merryn", "Pengelly", "", club_run_1="parish", club_run_2="parish")
    create_club_membership(db, "Benesek", "Tredinnick", "Ben", club_run_1="bowls", club_run_2="forrest")
    create_club_membership(db, "Enigoe", "Tredinnick", "Gogo", club_run_1="forrest", club_run_2="forrest")
    create_club_membership(db, "Rosenwyn", "Jelbert", "Roz", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Gwynnever", "Roseveare", "", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Locryn", "Chenoweth", "Lock", club_run_1="parish", club_run_2="parish")
    create_club_membership(db, "Oscar", "Fitzwilliam", "", club_run_1="bowls", club_run_2="parish")
    create_club_membership(db, "Sevi", "Jelbert", "", club_run_1="parish", club_run_2="parish")
    create_club_membership(db, "Tegen", "Chenoweth", "", club_run_1="bowls", club_run_2="wi")
    create_club_membership(db, "Caradoc", "Grose", "Carry", club_run_1="forrest", club_run_2="bowls")
    create_club_membership(db, "Demelza", "Jelbert", "Demi", club_run_1="computer", club_run_2="computer")
    create_club_membership(db, "Paul", "Smith", "", club_run_1="forrest", club_run_2="forrest")
    create_club_membership(db, "Faythely", "Pengelly", "Fayth", club_run_1="wi", club_run_2="forrest")
    create_club_membership(db, "Wendy", "Kempthorne", "", club_run_1="bowls", club_run_2="computer")
    create_club_membership(db, "Noah", "Angwin", "", club_run_1="forrest", club_run_2="bowls")
    create_club_membership(db, "Kenwyn", "Boscawen", "Kenny", club_run_1="computer", club_run_2="computer")
    create_club_membership(db, "John", "Smith", "", club_run_1="parish", club_run_2="parish")
    create_club_membership(db, "Linda", "Smith", "", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Henry", "Kempthorne", "", club_run_1="bowls", club_run_2="bowls", title_run_1="captain",
                           title_run_2="captain")
    create_club_membership(db, "Ursilla", "Chenoweth", "Silla", club_run_1="parish",
                           club_run_2="wi", title_run_1="aspirant")
    create_club_membership(db, "Yannick", "Berkowitz", "Yann", club_run_1="forrest", club_run_2="bowls",
                           title_run_1="aspirant")
    create_club_membership(db, "Veronica", "Kempthorne", "", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Zachary", "Angwin", "", club_run_1="forrest", club_run_2="bowls",
                           title_run_1="aspirant")
    create_club_membership(db, "Iger", "Moon", "", club_run_1="computer", club_run_2="computer")
    create_club_membership(db, "Xenara", "Moon", "", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Josep", "Boscawen", "Jo", club_run_1="forrest", club_run_2="forrest")
    create_club_membership(db, "Davydh", "Roseveare", "", club_run_1="parish", club_run_2="parish")
    create_club_membership(db, "Anneth", "Enys", "", club_run_1="forrest", club_run_2="forrest")
    create_club_membership(db, "Stefan", "Roseveare", "Stef", club_run_1="bowls", club_run_2="bowls")
    create_club_membership(db, "Felicity", "Kempthorne", "", club_run_1="wi", club_run_2="wi", title_run_1="chairwoman",
                           title_run_2="chairwoman")
    create_club_membership(db, "Georgina", "Czerny", "", club_run_1="computer", club_run_2="wi")
    create_club_membership(db, "Ross", "Thomas", "", club_run_1="parish", club_run_2 = "")
    create_club_membership(db, "Tressa", "Moon", "", club_run_1="computer", club_run_2="computer")
    create_club_membership(db, "Philippa", "Tredinnick", "Pippa", club_run_1="computer", club_run_2="computer")
    create_club_membership(db, "Lowen", "Grose", "", club_run_1="parish", club_run_2="parish")
    create_club_membership(db, "Blake", "Fitzwilliam", "", club_run_1="bowls", club_run_2="forrest",
                           title_run_1="aspirant")
    create_club_membership(db, "Ollie", "Moon", "Ollie", club_run_1="computer", club_run_2="forrest",
                           title_run_1="aspirant")
    create_club_membership(db, "Nathan", "Foxton", "Nate", club_run_1="computer", club_run_2="forrest",
                           title_run_1="aspirant")
    create_club_membership(db, "Eric", "McCormick", "", club_run_1="bowls", club_run_2="computer",
                           title_run_1="aspirant")
    create_club_membership(db, "Hedra", "Tredinnick", "", club_run_1="computer", club_run_2="computer")
    create_club_membership(db, "Chessen", "Angwin", "", club_run_1="wi", club_run_2="parish")
    create_club_membership(db, "Willym", "Enys", "", club_run_1="parish", club_run_2="computer")
    create_club_membership(db, "Androw", "Redruth", "", club_run_1="bowls",
                           club_run_2="forrest")
    create_club_membership(db, "Dorian", "Carter", "", club_run_1="forrest", club_run_2="")
    create_club_membership(db, "Freya", "Mully", "", club_run_1="forrest", club_run_2="forrest")
    create_club_membership(db, "Thomas", "Hammond", "", club_run_1="parish", club_run_2="parish",
                           title_run_1="aspirant", title_run_2="aspirant")
    create_club_membership(db, "Selina", "Blair", "", club_run_1="wi", club_run_2="bowls", title_run_2="aspirant")
    create_club_membership(db, "Maren", "Nilsen", "", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Isette", "Redruth", "", club_run_1="forrest", club_run_2="forrest",
                           title_run_1="leader", title_run_2="leader")
    create_club_membership(db, "Ales", "Thomas", "", club_run_1="parish", club_run_2="parish", title_run_1="chairwoman",
                           title_run_2="chairwoman")
    create_club_membership(db, "Hykka", "Jelbert", "", club_run_1="bowls", club_run_2="forrest")
    create_club_membership(db, "Newlyn", "Czerny", "Noo", club_run_1="computer", club_run_2="bowls",
                           title_run_2="aspirant")
    create_club_membership(db, "Jorun", "Nilsen", "", club_run_1="parish", club_run_2="parish", title_run_1="aspirant",
                           title_run_2="aspirant")
    create_club_membership(db, "Victor", "Czerny", "", club_run_1="forrest", club_run_2="computer",
                           title_run_1="aspirant")
    create_club_membership(db, "Remi", "Grigorio", "", club_run_1="computer",
                           club_run_2="forrest", title_run_1="aspirant", title_run_2="aspirant")
    create_club_membership(db, "Kate", "Astell", "", club_run_1="wi", club_run_2="wi")
    create_club_membership(db, "Greg", "Borromead", "", club_run_1="bowls", club_run_2="bowls")
    create_club_membership(db, "Fenella", "Borromead", "", club_run_1="computer", club_run_2="computer")


def seed_database(db: Session):
    # Add the default stuff in the database
    db_state = models.RunState()
    db.add(db_state)
    _seed_predictions(db)
    _seed_questions(db)
    _seed_recipe_messages(db)
    _seed_alien_messages(db)
    _seed_club_memberships(db)

    # Authors
    create_author(db, "Jaime", "Test")

    create_author(db, "admin", "somepassword")

    create_author(db, "admin", "somepassword")
    _seed_news_articles(db)

    from .main import characters
    for character in characters:
        create_author(db, character.first_name, character.last_name)

    # TEST USER
    #create_club_membership(db, "Jaime", "van Kessel", "Nallath", club_run_1="FrivolousEngineering", club_run_2="FrivolousEngineering", title_run_1="Chief untouchable engineering", title_run_2="Chief untouchable engineering")
    #create_club_membership(db, "Corne", "van Kessel", "BlazingEclipse", club_run_1="FrivolousEngineering", club_run_2="FrivolousEngineering", title_run_1="Chief touchable Engineering", title_run_2="Chief touchable Engineering")
    # Left title empty on purpose for testing purposes
    #create_club_membership(db, "Roos", "Schultheiss", "Fjadderal", club_run_1="FrivolousEngineering", club_run_2="FrivolousEngineering", title_run_1="", title_run_2="")

    #create_club_membership(db, "Felicity", "Kempthorne", "", club_run_1="wi", club_run_2="wi", title_run_1="Chairwomen", title_run_2="Chairwomen")

    #create_club_membership(db, "Rosenwyn", "Jelbert", "Roz", club_run_1="wi", club_run_2="wi")
