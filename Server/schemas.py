from enum import Enum

from pydantic import BaseModel
from typing import Optional, List


class QuestionType(str, Enum):
    boolean: str = "boolean"
    freeform: str = "freeform"
    pickone: str = "pickone"
    pickmultiple: str = "pickmultiple"

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
    type: QuestionType

    required: bool


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





