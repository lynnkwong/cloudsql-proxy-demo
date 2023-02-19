from pydantic import BaseSettings, Field, SecretStr
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.schema import MetaData

# Create a base for SQLAlchemy mappers.
Base = declarative_base(metadata=MetaData(schema="app"))
metadata = Base.metadata


# A Pydantic model to get environment variables.
class DbSettings(BaseSettings):
    """Settings for SQL."""

    host: str = Field(..., env="DB_HOST")
    user: str = Field(..., env="DB_USERNAME")
    password: SecretStr = Field(..., env="DB_PASSWORD")
    port: int = Field(env="DB_PORT", default=3306)
    db_name: str = Field(env="DB_NAME", default="app")

# We need to create an instance of the Pydantic model to access the
# environment variables.
db_settings = DbSettings()

db_conn_url = (
    "mysql+pymysql://"
    f"{db_settings.user}:{db_settings.password.get_secret_value()}"
    f"@{db_settings.host}:{db_settings.port}/{db_settings.db_name}"
)

# Create SQLAlchemy SQL engine and session factory.
engine = create_engine(db_conn_url)
session_factory = sessionmaker(bind=engine)
scoped_session_factory = scoped_session(session_factory)


def get_db_sess():
    """Get a SQLAlchemy ORM Session instance.

    Yields:
        A SQLAlchemy ORM Session instance.
    """
    db_session: Session = scoped_session_factory()
    try:
        yield db_session
    except Exception as exc:
            db_session.rollback()
            raise exc
    finally:
        db_session.close()
