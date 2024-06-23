from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder

from . import crud, models, schemas
from .database import SessionLocal, engine

origins = [
    "http://localhost:3000",
    "localhost:3000"
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


    #option = schemas.OptionCreate(question_id=question_id)

    #return crud.create_question(db=db, question=question)


@app.delete("/questions/{question_id}/")
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    if crud.get_question(db, question_id) is None:
        raise HTTPException(status_code=404, detail="Question not found")

    crud.delete_question(db, question_id)


