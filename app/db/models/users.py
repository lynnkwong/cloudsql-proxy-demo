from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import SMALLINT

from app.db.db import Base

class User(Base):
    """An ORM class for table `app.users`."""
    __tablename__ = "users"
    __table_args__ = {"schema": "app"}

    id = Column(SMALLINT, primary_key=True)
    name = Column(
        String(50),
        nullable=False,
    )
    job = Column(
        String(50),
        server_default=text("''"),
    )
