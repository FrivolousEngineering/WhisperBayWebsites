from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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