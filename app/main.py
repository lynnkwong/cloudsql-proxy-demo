from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db.db import get_db_sess
from app.db.models.users import User as UserModel
from app.schema.users import User as UserSchema

app = FastAPI()


@app.get("/users")
async def get_users(
    db_sess: Session = Depends(get_db_sess),
) -> list[UserSchema]:
    users = db_sess.query(UserModel).all()

    return users
