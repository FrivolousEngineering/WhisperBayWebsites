from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine

origins = [
    "*"
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
               "WhisperBay Community Garden": "../CommunityGarden/home.html"}


food_webring = ["Cornish Food Delights", "Womens Institute", "WhisperBay Community Garden"]

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


@app.post("/evaluateAnswers/")
async def post_answers(request: Request, db: Session = Depends(get_db)):
    da = await request.form()
    da = jsonable_encoder(da)

    return {"answer": "There is a bright future for you! You are so amazing!"}
    pass


@app.post("/reset/")
async def reset_database( db: Session = Depends(get_db)):
    crud.reset_database(db)
    crud.seed_database(db)


@app.get("/webring/",  response_model=schemas.WebRing)
async def get_webring(site: str):
    active_webring = []
    webring_name = ""

    # Find what webring was activated
    if site in food_webring:
        active_webring = food_webring
        webring_name = "Food"

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

