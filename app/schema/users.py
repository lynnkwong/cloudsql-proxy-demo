from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    job: str

    class Config:
        orm_mode = True
