from pydantic import BaseModel

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