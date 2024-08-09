from enum import Enum

from pydantic import BaseModel
from typing import Optional, List



class QuestionType(str, Enum):
    boolean: str = "boolean"
    freeform: str = "freeform"
    pickone: str = "pickone"
    pickmultiple: str = "pickmultiple"
    integer: int = "integer"


class WebRing(BaseModel):
    next_site_url: str
    next_site_name: str
    name: str
    previous_site_url: str
    previous_site_name: str


class GuestbookMessageBase(BaseModel):
    author_name: str
    message: str
    target_board: str


class GuestbookMessageCreate(GuestbookMessageBase):
    pass


class GuestbookMessage(GuestbookMessageBase):
    id: int
    time: str

    class Config:
        orm_mode = True


class QuestionOptionBase(BaseModel):

    value: str
    pass


class QuestionOptionCreate(QuestionOptionBase):
    pass


class QuestionOption(QuestionOptionBase):
    order: int
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


# A user that can create news articles
class AuthorBase(BaseModel):
    name: str
    password: str


class AuthorSummary(AuthorBase):
    id: int


class NewsArticlesBase(BaseModel):
    title: str
    time: str
    text: str


class ClubMembership(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    title: str


class NewsArticle(NewsArticlesBase):
    id: int
    author: AuthorSummary
    class Config:
        orm_mode = True


class Author(AuthorSummary):
    articles: List["NewsArticle"]

    class Config:
        orm_mode = True






