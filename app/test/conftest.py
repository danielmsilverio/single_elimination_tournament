from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from dotenv import load_dotenv
import pytest

load_dotenv("envs/test.env", override=True)

from app.src.core.configs import Settings

POSTGRES_DB_TEST = f"{Settings().POSTGRES_DB}"
DB_URL_TEST = f"{Settings().DB_URL_BASE}/{POSTGRES_DB_TEST}"


@pytest.fixture(scope="session", autouse=True)
def fake_db():
    if database_exists(DB_URL_TEST):
        print(f"Dropping database {POSTGRES_DB_TEST}")
        drop_database(DB_URL_TEST)

    print(f"Creating database {POSTGRES_DB_TEST}")
    create_database(DB_URL_TEST)
    print(f"Database {POSTGRES_DB_TEST} created")

    print(f"Inicializing database {POSTGRES_DB_TEST}")
    engine = create_engine(DB_URL_TEST)
    from app.src.models.tournament import Tournament
    from app.src.models.match import Match
    from app.src.core.database import SessionLocal, Base

    db = SessionLocal()
    Base.metadata.create_all(engine)
    print(f"The {POSTGRES_DB_TEST} ready")
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
