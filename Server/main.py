from typing import Annotated, List, Dict, Any

from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine
import re

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from .advice import generate_relation_advice, generate_professional_advice
from .schemas import AnswerCreate

app = FastAPI(docs_url=None, redoc_url=None)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

origins = [
    "*"
]

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="Server/static"), name="static")


known_sites = {"Cornish Food Delights": "../CornishFood/index.html",
               "Womens Institute": "../WomenInstitute/index.html",
               "WhisperBay Community Garden": "../CommunityGarden/home.html",
               "General Store": "../GeneralStore/index.htm",
               "Crystal Store": "../CrystalStore/index.htm",
               "Tourism Board": "../TourismBoard/welcome_tourism.html",
               "Holiday Park": "../CornishRiviera/index.html",
               "Computer Club": "../ComputerClub/index.html",
               "Forest School": "../ForrestSchool/index.html"}


food_webring = ["Cornish Food Delights", "Womens Institute", "WhisperBay Community Garden"]
commerce_webring = ["General Store", "Crystal Store", "Tourism Board", "Holiday Park"]
education_webring = ["Computer Club", "Forest School", "Womens Institute"]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/messages/", response_model=list[schemas.GuestbookMessage])
def get_messages(target_guestbook: str, db: Session = Depends(get_db)):
    messages = crud.get_guestbook_message_for_board(db, board = target_guestbook)
    return messages


@app.post("/messages/", response_model=schemas.GuestbookMessage)
def create_message(message: schemas.GuestbookMessageCreate, db: Session = Depends(get_db)):
    return crud.create_guestbook_message(db=db, message=message)

@app.post("/messages/form/", response_model=schemas.GuestbookMessage)
async def create_message_form(target_guestbook: str, request: Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)

    message = schemas.GuestbookMessageCreate(target_board = target_guestbook, author_name = da["name"], message = da["message"])
    return crud.create_guestbook_message(db=db, message=message)

@app.get("/questions/", response_model=list[schemas.Question])
def get_questions(db: Session = Depends(get_db)):
    return crud.get_questions(db)


@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)


@app.post("/questions/{question_id}/options/", response_model=schemas.QuestionOption)
def create_question_option(question_option: schemas.QuestionOptionCreate, question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail = "Question not found")
    return crud.create_question_option(db, question_id=question_id, question_option=question_option)


@app.post("/questions/{question_id}/answers/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.create_answer(db, question_id=question_id, answer=answer)


@app.put("/questions/{question_id}/")
async def update_question(question_id: int, request: Request, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")

    da = await request.form()
    da = jsonable_encoder(da)
    crud.update_question_text(db, question_id, da["text"])
    crud.update_question_type(db, question_id, da["type"])

    for option_key in (k for k in da if k.startswith("option")):
        option_id = int(option_key.replace("option_", ""))
        crud.update_option_text(db, option_id, da[option_key])
        print(option_key)

    print(da)


@app.post("/questions/empty/", response_model=schemas.Question)
def create_empty_question(db: Session = Depends(get_db)):
    question = schemas.QuestionCreate(text="", type="freeform", required=False)
    return crud.create_question(db=db, question=question)


@app.post("/questions/{question_id}/options/empty/") #, response_model=schemas.Question)
def create_empty_option(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    if question.type == "freeform" or question.type == "boolean":
        raise HTTPException(status_code=400, detail="Can't add options to freeform or boolean questions!")

    crud.create_question_option(db, question_id=question_id, question_option= schemas.QuestionOptionCreate(order = 0, value = ""))


@app.delete("/questions/{question_id}/")
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")

    crud.delete_question(db, question_id)



@app.delete("/options/{option_id}/")
async def delete_question(option_id: int, db: Session = Depends(get_db)):
    crud.delete_option(db, option_id)


def calculate_age_score(input_age: int, character_age: int) -> float:
    age_difference = abs(input_age - character_age)
    max_difference = 5

    if age_difference >= max_difference:
        return -1

    return (1 - (age_difference / max_difference))

# This is some debug code so that I can work with the hapyness 2000 matching testing
class Character(BaseModel):
    first_name: str
    last_name: str
    gender_run1: str
    gender_run2: str
    profession: str
    age: int
    relationship_status: str
    children: bool
    contact_with_siblings: str
    star_sign: str

characters = [
    Character(first_name="Aswen", last_name="Pengelly", gender_run1="Female", gender_run2="Female", age=41, profession="Professional", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Capricorn"),
    Character(first_name="Merryn", last_name="Pengelly", gender_run1="Male", gender_run2="Male", age=42, profession="Professional", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Aquarius"),
    Character(first_name="Benesek", last_name="Tredinnick", gender_run1="Male", gender_run2="Male", age=50, profession="Business owner", relationship_status="Widowed", children=True, contact_with_siblings="I don't have siblings", star_sign="Pisces"),
    Character(first_name="Enigoe", last_name="Tredinnick", gender_run1="Male", gender_run2="Male", age=25, profession="Unemployed", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Aries"),
    Character(first_name="Rosenwyn", last_name="Jelbert", gender_run1="Female", gender_run2="Female", age=26, profession="Manual", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Aries"),
    Character(first_name="Gwynnever", last_name="Roseveare", gender_run1="Female", gender_run2="Female", age=24, profession="Manual", relationship_status="Married", children=False, contact_with_siblings="Yes", star_sign="Gemini"),
    Character(first_name="Locryn", last_name="Chenoweth", gender_run1="Male", gender_run2="Male", age=46, profession="Business owner", relationship_status="Widowed", children=True, contact_with_siblings="No", star_sign="Cancer"),
    Character(first_name="Oscar", last_name="Fitzwilliam", gender_run1="Male", gender_run2="Male", age=41, profession="Public services", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Leo"),
    Character(first_name="Sevi", last_name="Jelbert", gender_run1="Female", gender_run2="Male", age=44, profession="Business owner", relationship_status="Separated", children=True, contact_with_siblings="No", star_sign="Libra"),
    Character(first_name="Tegen", last_name="Chenoweth", gender_run1="Female", gender_run2="Female", age=20, profession="Manual", relationship_status="Engaged", children=False, contact_with_siblings="Yes", star_sign="Libra"),
    Character(first_name="Caradoc", last_name="Grose", gender_run1="Male", gender_run2="Male", age=23, profession="Manual", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Scorpio"),
    Character(first_name="Demelza", last_name="Jelbert", gender_run1="Female", gender_run2="Female", age=18, profession="Student", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Sagittarius"),
    Character(first_name="Paul", last_name="Smith", gender_run1="Male", gender_run2="Male", age=18, profession="Student", relationship_status="In a relationship", children=False, contact_with_siblings="I don't have siblings", star_sign="Capricorn"),
    Character(first_name="Faythely", last_name="Pengelly", gender_run1="Female", gender_run2="Female", age=18, profession="Student", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Aquarius"),
    Character(first_name="Wendy", last_name="Kempthorne", gender_run1="Female", gender_run2="Female", age=18, profession="Student", relationship_status="Single", children=False, contact_with_siblings="I don't have siblings", star_sign="Pisces"),
    Character(first_name="Noah", last_name="Angwin", gender_run1="Male", gender_run2="Male", age=18, profession="Student", relationship_status="Single", children=False, contact_with_siblings="I don't have siblings", star_sign="Aries"),
    Character(first_name="Kenwyn", last_name="Boscawen", gender_run1="Female", gender_run2="Male", age=34, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Taurus"),
    Character(first_name="John", last_name="Smith", gender_run1="Male", gender_run2="Male", age=40, profession="Public services", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Gemini"),
    Character(first_name="Linda", last_name="Smith", gender_run1="Female", gender_run2="Female", age=40, profession="Business owner", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Cancer"),
    Character(first_name="Henry", last_name="Kempthorne", gender_run1="Male", gender_run2="Male", age=45, profession="Business owner", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Leo"),
    Character(first_name="Ursilla", last_name="Chenoweth", gender_run1="Female", gender_run2="Female", age=45, profession="Creative", relationship_status="???", children=False, contact_with_siblings="No", star_sign="Virgo"),
    Character(first_name="Yannick", last_name="Berkowitz", gender_run1="Male", gender_run2="Female", age=45, profession="Creative", relationship_status="Widowed", children=False, contact_with_siblings="No", star_sign="Libra"),
    Character(first_name="Veronica", last_name="Kempthorne", gender_run1="Female", gender_run2="Female", age=99, profession="Business owner", relationship_status="Single", children=False, contact_with_siblings="No", star_sign="Scorpio"),
    Character(first_name="Zachary", last_name="Angwin", gender_run1="Male", gender_run2="Male", age=35, profession="Creative", relationship_status="Divorced", children=True, contact_with_siblings="No", star_sign="Sagittarius"),
    Character(first_name="Iger", last_name="Moon", gender_run1="Male", gender_run2="Male", age=48, profession="Business owner", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Capricorn"),
    Character(first_name="Xenara", last_name="Moon", gender_run1="Female", gender_run2="Female", age=49, profession="Business owner", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Aquarius"),
    Character(first_name="Josepa", last_name="Boscawen", gender_run1="Female", gender_run2="Male", age=27, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Pisces"),
    Character(first_name="Davydh", last_name="Roseveare", gender_run1="Male", gender_run2="Male", age=40, profession="Manual", relationship_status="???", children=True, contact_with_siblings="No", star_sign="Aries"),
    Character(first_name="Anneth", last_name="Enys", gender_run1="Female", gender_run2="Female", age=26, profession="Business owner", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Taurus"),
    Character(first_name="Stefan", last_name="Roseveare", gender_run1="Male", gender_run2="Male", age=22, profession="Business owner", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Gemini"),
    Character(first_name="Felicity", last_name="Kempthorne", gender_run1="Female", gender_run2="Female", age=45, profession="Public services", relationship_status="Married", children=True, contact_with_siblings="No", star_sign="Cancer"),
    Character(first_name="Georgina", last_name="Czerny", gender_run1="Female", gender_run2="Female", age=37, profession="Public services", relationship_status="???", children=False, contact_with_siblings="Yes", star_sign="Leo"),
    Character(first_name="Ross", last_name="Thomas", gender_run1="Male", gender_run2="Male", age=48, profession="Public services", relationship_status="Married", children=False, contact_with_siblings="No", star_sign="Virgo"),
    Character(first_name="Tressa", last_name="Moon", gender_run1="Female", gender_run2="Female", age=26, profession="Public services", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Libra"),
    Character(first_name="Philippa", last_name="Tredinnick", gender_run1="Female", gender_run2="Female", age=32, profession="Public services", relationship_status="???", children=False, contact_with_siblings="Yes", star_sign="Scorpio"),
    Character(first_name="Lowen", last_name="Grose", gender_run1="Male", gender_run2="Male", age=35, profession="Public services", relationship_status="???", children=False, contact_with_siblings="Yes", star_sign="Aquarius"),
    Character(first_name="Blake", last_name="Fitzwilliam", gender_run1="Female", gender_run2="Male", age=35, profession="Unemployed", relationship_status="???", children=False, contact_with_siblings="Yes", star_sign="Capricorn"),
    Character(first_name="Olivia", last_name="Moon", gender_run1="Male", gender_run2="Female", age=24, profession="Unemployed", relationship_status="???", children=False, contact_with_siblings="Yes", star_sign="Aquarius"),
    Character(first_name="Nathan", last_name="Foxton", gender_run1="Male", gender_run2="Male", age=26, profession="Unemployed", relationship_status="???", children=False, contact_with_siblings="No", star_sign="Pisces"),
    Character(first_name="Eric", last_name="McCormick", gender_run1="Male", gender_run2="Male", age=53, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="No", star_sign="Aries"),
    Character(first_name="Hedra", last_name="Tredinnick", gender_run1="Female", gender_run2="Female", age=25, profession="Public services", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Taurus"),
    Character(first_name="Chessen", last_name="Angwin", gender_run1="Female", gender_run2="Female", age=35, profession="Public services", relationship_status="???", children=True, contact_with_siblings="Yes", star_sign="Gemini"),
    Character(first_name="Willym", last_name="Enys", gender_run1="Male", gender_run2="Male", age=30, profession="Public services", relationship_status="In a relationship", children=False, contact_with_siblings="Yes", star_sign="Cancer"),
    Character(first_name="Androw", last_name="Redruth", gender_run1="Male", gender_run2="Male", age=20, profession="Public services", relationship_status="Engaged", children=False, contact_with_siblings="Yes", star_sign="Leo"),
    Character(first_name="Dorian", last_name="Carter", gender_run1="Male", gender_run2="Male", age=39, profession="Public services", relationship_status="Single", children=False, contact_with_siblings="No", star_sign="Sagittarius"),
    Character(first_name="Freya", last_name="Mully", gender_run1="Female", gender_run2="Female", age=34, profession="Public services", relationship_status="Single", children=False, contact_with_siblings="No", star_sign="Libra"),
    Character(first_name="Thomas", last_name="Hammond", gender_run1="Male", gender_run2="Male", age=40, profession="Professional", relationship_status="In a relationship", children=False, contact_with_siblings="No", star_sign="Scorpio"),
    Character(first_name="Selina", last_name="Blair", gender_run1="Female", gender_run2="Female", age=39, profession="Professional", relationship_status="???", children=False, contact_with_siblings="No", star_sign="Sagittarius"),
    Character(first_name="Maren", last_name="Nilsen", gender_run1="Female", gender_run2="Female", age=26, profession="Student", relationship_status="Single", children=False, contact_with_siblings="I don't have siblings", star_sign="Capricorn"),
    Character(first_name="Isette", last_name="Redruth", gender_run1="Female", gender_run2="Female", age=34, profession="Student", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Aquarius"),
    Character(first_name="Ales", last_name="Thomas", gender_run1="Female", gender_run2="Female", age=41, profession="Professional", relationship_status="Married", children=False, contact_with_siblings="No", star_sign="Pisces"),
    Character(first_name="Richelle", last_name="Jelbert", gender_run1="Male", gender_run2="Female", age=46, profession="Unemployed", relationship_status="Separated", children=True, contact_with_siblings="No", star_sign="Aries"),
    Character(first_name="Newlyn", last_name="Czerny", gender_run1="Female", gender_run2="Female", age=33, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="Yes", star_sign="Taurus"),
    Character(first_name="Jorun", last_name="Nilsen", gender_run1="Female", gender_run2="Female", age=47, profession="Manual", relationship_status="Single", children=True, contact_with_siblings="No", star_sign="Gemini"),
    Character(first_name="Victor", last_name="Czerny", gender_run1="Male", gender_run2="Male", age=37, profession="Professional", relationship_status="Married", children=False, contact_with_siblings="Yes", star_sign="Cancer"),
    Character(first_name="Remi", last_name="Grigorio", gender_run1="Male", gender_run2="Male", age=40, profession="Creative", relationship_status="Married", children=False, contact_with_siblings="No", star_sign="Leo"),
    Character(first_name="Kate", last_name="Astell", gender_run1="Female", gender_run2="Female", age=42, profession="Creative", relationship_status="Married", children=False, contact_with_siblings="No", star_sign="Virgo"),
    Character(first_name="Greg", last_name="Borromead", gender_run1="Male", gender_run2="Male", age=30, profession="Creative", relationship_status="Married", children=False, contact_with_siblings="No", star_sign="Libra"),
    Character(first_name="Fenella", last_name="Borromead", gender_run1="Female", gender_run2="Female", age=28, profession="Unemployed", relationship_status="Married", children=False, contact_with_siblings="Yes", star_sign="Scorpio")
]


def calc_relationship_status_score(input_status: str, character_status: str) -> float:
    if input_status == character_status:
        return 1.

    # Define likely changes
    likely_changes = {
        ("Single", "In a relationship"): 0.80,
        ("In a relationship", "Single"): 0.80,
        ("In a relationship", "Engaged"): 0.80,
        ("Engaged", "In a relationship"): 0.80,
        ("Widowed", "In a relationship"): 0.80,
        ("Widowed", "Married"): 0.8,  # Change likely for Locryn Chenoweth
        ("Widowed", "Separated"): 0.8,  # Change likely for Locryn Chenoweth
        ("Single", "Engaged"): 0.50,
        ("Engaged", "Single"): 0.60,
        ("Engaged", "Separated"): 0.50,
        ("Separated", "Engaged"): 0.50,
        ("Separated", "In a relationship"): 0.70
    }

    # Check for transitions in likely changes
    if (input_status, character_status) in likely_changes:
        return likely_changes[(input_status, character_status)]
    if (character_status, input_status) in likely_changes:
        return likely_changes[(character_status, input_status)]

    # For all other cases, no match
    return 0


def calc_profession_score(input_profession: str, character_profession: str) -> float:
    if input_profession == character_profession:
        return 1

    # Define likely transitions
    likely_transitions = {
        ("Unemployed", "Professional"): 0.70,
        ("Professional", "Unemployed"): 0.70,
        ("Unemployed", "Business owner"): 0.70,
        ("Business owner", "Unemployed"): 0.70,
        ("Unemployed", "Creative"): 0.70,
        ("Creative", "Unemployed"): 0.70,
        ("Unemployed", "Public services"): 0.70,
        ("Public services", "Unemployed"): 0.70,
        ("Unemployed", "Manual"): 0.70,
        ("Manual", "Unemployed"): 0.70,
        ("Business owner", "Creative"): 0.80,
        ("Creative", "Business owner"): 0.80,
        ("Manual", "Public services"): 0.50,
        ("Public services", "Manual"): 0.50,
        ("Creative", "Professional"): 0.50,
        ("Professional", "Creative"): 0.50,
    }

    # Check for transitions in likely transitions
    if (input_profession, character_profession) in likely_transitions:
        return likely_transitions[(input_profession, character_profession)]
    if (character_profession, input_profession) in likely_transitions:
        return likely_transitions[(character_profession, input_profession)]

    # For all other cases, no match
    return 0


def extract_question_answers(input_dict):
    result = {}
    pattern = re.compile(r'^question_(\d+)_answer$')

    for key, value in input_dict.items():
        match = pattern.match(key)
        if match:
            number = match.group(1)
            result[number] = value

    return result


@app.get("/answers/", response_model=List[schemas.Answer])
def get_answers(db: Session = Depends(get_db)):
    return db.query(models.Answer).all()

@app.get("/answers_by_submission/", response_model=List[Dict[str, Any]])
def get_answers_by_submission(db: Session = Depends(get_db)):
    submissions = db.query(models.Answer.submission_id).distinct().all()
    result = []

    for submission in submissions:
        submission_id = submission[0]
        answers = db.query(models.Answer).filter(models.Answer.submission_id == submission_id).all()

        submission_data = {"submission_id": submission_id}
        for answer in answers:
            question_text = answer.question.text
            submission_data[question_text] = answer.value

        result.append(submission_data)

    return result

@app.post("/evaluateAnswers/")
async def post_answers(request: Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)

    best_match = None
    highest_score = 0
    run_number = 1 # TODO: hardcoded run
    answers = extract_question_answers(da)

    submission_id = crud.get_highest_submission_id(db) + 1
    for question_id, answer in answers.items():
        created_answer = crud.add_answer(db=db, answer=AnswerCreate.parse_obj({"value":answer, "question_id": question_id, "submission_id": submission_id}))

    # Yeah i didn't build this in the greatest way. Whatever
    age = int(da["question_1_answer"])
    gender = da["question_2_answer"]
    profession = da["question_3_answer"]
    relation_status = da["question_4_answer"]
    starsign = da["question_5_answer"]

    weights = {"age": 3, "gender": 6, "profession": 2, "relation_status": 2, "starsign": 5}

    # 3 for macthing the age, 6 for matching the gender, and 1 for children, 2 for profession, 2 for relation, 1 for siblings
    highest_score_possible = 3 + 6 + 2 + 2 + 1 + 1 + 5

    # Loop over all characters and figure out wich of them match the best
    for character in characters:
        age_score = calculate_age_score(age, character.age) * weights["age"]

        if run_number == 1:
            gender_score = int(gender == character.gender_run1)
        else:
            gender_score = int(gender == character.gender_run2)

        # Since gender isn't something that the players will fuck up, i'm giving that a lot more weight.
        gender_score *= weights["gender"]

        # Relationship has a bit more of a fuzzy match as it can change.
        relationship_score = calc_relationship_status_score(relation_status, character.relationship_status) * weights["relation_status"]

        # Profession also has a bit of fuzzy matching going on
        profession_score = calc_profession_score(profession, character.profession) * weights["profession"]

        starsign_score = int(starsign == character.star_sign) * weights["starsign"]
        # We count the children score as less, as it has fewer options (and is thus less indicative)
        total_score = (gender_score + age_score + profession_score + relationship_score + starsign_score)

        if total_score > highest_score:
            highest_score = total_score
            best_match = character

            found_scores = (gender_score, age_score, profession_score, relationship_score, starsign_score)

    print(da)
    print(age, gender)

    print(f"The best match is {best_match.first_name} {best_match.last_name} with a score of {highest_score}, [{found_scores}]")

    individual_vs_collectivist = "neutral"
    agnostic_vs_spiritual = "neutral"
    progressive_vs_conservative = "neutral"

    if highest_score < highest_score_possible / 4 * 3:
        result = "Although we were able to generate some advice for you, it is not as good as we would like it to be!"
    else:
        result = "Here is your personalized advice!"

    extra_advice = []
    relation_advice = generate_relation_advice(relation_status, individual_vs_collectivist, agnostic_vs_spiritual,
                                                     progressive_vs_conservative)
    professional_advice = generate_professional_advice(profession, individual_vs_collectivist, agnostic_vs_spiritual, progressive_vs_conservative)

    if relation_advice:
        extra_advice.append("<h1>Relation advice</h1>")
        extra_advice.extend(relation_advice)
    if professional_advice:
        extra_advice.append("<h1>Professional advice</h1>")
        extra_advice.extend(professional_advice)

    for line in extra_advice:
        result += f"</br> {line}"
    return {"answer": result, "match": f"{best_match.first_name} {best_match.last_name}", "score": highest_score}
    pass


@app.post("/reset/")
async def reset_database(db: Session = Depends(get_db)):
    crud.reset_database(db)
    crud.seed_database(db)


@app.get("/webring/",  response_model=schemas.WebRing)
async def get_webring(site: str, ring: str = ""):
    active_webring = []
    webring_name = ""

    if ring == "food":
        active_webring = food_webring
        webring_name = "Food"
    if ring == "commerce":
        active_webring = commerce_webring
        webring_name = "Commerce"
    if ring == "education":
        active_webring = education_webring
        webring_name = "Education"
    if active_webring:
        webring_index = active_webring.index(site)
        next_index = webring_index + 1
        prev_index = webring_index - 1

        if prev_index < 0:
            prev_index = len(active_webring) - 1

        if next_index > len(active_webring) - 1:
            next_index = 0
        prev_name = active_webring[prev_index]
        next_name = active_webring[next_index]
        prev_url = known_sites[prev_name]
        next_url = known_sites[next_name]
        return schemas.WebRing(next_site_url = next_url, next_site_name = next_name, previous_site_name = prev_name, previous_site_url = prev_url, name = webring_name)
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/authors/",  response_model=list[schemas.Author])
async def get_authors(db: Session = Depends(get_db)):
    for result in crud.get_authors(db):
        print(result.name)
    return crud.get_authors(db)


@app.post("/authors/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):
    login_details_correct = crud.check_author_username_password_valid(db, username, password)
    if not login_details_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"username": username}


@app.post("/newsarticles/")
async def post_newsarticle(username: Annotated[str, Form()], article_subject: Annotated[str, Form()], article_text: Annotated[str, Form()], db: Session = Depends(get_db)):
    crud.create_news_article(db, username = username, article_subject = article_subject, article_text=article_text)
    return {}

@app.get("/newsarticles/", response_model=list[schemas.NewsArticle])
async def get_newsarticle(db: Session = Depends(get_db)):
    return crud.get_news_articles(db)


@app.get("/clubmemberships/", response_model=list[schemas.ClubMembership])
async def get_memberships(club: str, db: Session = Depends(get_db)):
    # Todo: maybe also add some handling if the club wasn't recognised.
    return crud.get_all_club_members_by_club(db, club)