from pydantic import BaseModel
from typing import Optional, List

class GuestbookMessageBase(BaseModel):
    author_name: str
    message: str
    target_board: str

class GuestbookMessageCreate(GuestbookMessageBase):
    pass


class GuestbookMessage(GuestbookMessageBase):
    id: int

    class Config:
        orm_mode = True


class QuestionOptionBase(BaseModel):
    order: int
    value: str
    pass


class QuestionOptionCreate(QuestionOptionBase):
    pass


class QuestionOption(QuestionOptionBase):
    id: int
    pass

class AnswerBase(BaseModel):
    pass


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    pass


class QuestionBase(BaseModel):
    text: str
    type: str

    required: bool
    type: str


class QuestionCreate(QuestionBase):
    order: Optional[int] = None
    pass


class Question(QuestionBase):
    id: int
    order: int
    answers: Optional[List["Answer"]]
    options: Optional[List["QuestionOption"]]
    class Config:
        orm_mode = True





