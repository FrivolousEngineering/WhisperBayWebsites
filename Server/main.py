from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine


from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

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
    max_difference = 20  # You can adjust this value based on your needs

    if age_difference >= max_difference:
        return 0.0  # No match if the difference is too large

    return (1 - (age_difference / max_difference))

# This is some debug code so that I can work with the hapyness 2000 matching testing
class Character(BaseModel):
    first_name: str
    last_name: str
    gender_run_1: str
    gender_run_2: str
    profession: str
    age: int
    relationship_status: str
    children: bool
    contact_with_siblings: str


characters = [
    Character(first_name="Aswen", last_name="Pengelly", gender_run1="Female", gender_run2="Female", age=42, profession="Professional", relationship_status="Married", children=True, contact_with_siblings="No"),
    Character(first_name="Merryn", last_name="Pengelly", gender_run1="Male", gender_run2="Male", age=43, profession="Professional", relationship_status="Married", children=True, contact_with_siblings="No"),
    Character(first_name="Oscar", last_name="Fitzwilliam", gender_run1="Male", gender_run2="Male", age=40, profession="Public services", relationship_status="Single", children=False, contact_with_siblings="Yes"),
    Character(first_name="Veronica", last_name="Kempthorne", gender_run1="Female", gender_run2="Female", age=39, profession="Business owner", relationship_status="Single", children=False, contact_with_siblings="No"),
    Character(first_name="Sevi", last_name="Jelbert", gender_run1="Female", gender_run2="Male", age=41, profession="Business owner", relationship_status="Separated", children=True, contact_with_siblings="No"),
    Character(first_name="Locryn", last_name="Chenoweth", gender_run1="Male", gender_run2="Male", age=45, profession="Business owner", relationship_status="Widowed", children=True, contact_with_siblings="No"),
    Character(first_name="Tressa", last_name="Moon", gender_run1="Female", gender_run2="Female", age=28, profession="Public services", relationship_status="In a relationship", children=False, contact_with_siblings="Yes"),
    Character(first_name="Oliver", last_name="Moon", gender_run1="Male", gender_run2="Female", age=24, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="Yes"),
    Character(first_name="Nathan", last_name="Foxton", gender_run1="Male", gender_run2="Male", age=29, profession="Unemployed", relationship_status="Single", children=False, contact_with_siblings="No"),
    Character(first_name="Anneth", last_name="Enys", gender_run1="Female", gender_run2="Female", age=26, profession="Business owner", relationship_status="In a relationship", children=False, contact_with_siblings="Yes"),
]


@app.post("/evaluateAnswers/")
async def post_answers(request: Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)

    best_match = None

    # Yeah i didn't built this in the greatest way. Whatever
    age = int(da["question_2_answer"])
    gender = da["question_3_answer"]

    # Loop over all characters and figure out wich of them match the best
    for character in characters:
        age_score = calculate_age_score(age, character.age)
        # TODO: hardcoded run
        gender_score = int(gender == character.gender_run1)

    print(age, gender)

    return {"answer": "There is a bright future for you! You are so amazing!"}
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