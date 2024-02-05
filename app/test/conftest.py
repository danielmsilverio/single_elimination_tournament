from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from dotenv import load_dotenv

from app.src.core.configs import Settings
import pytest

POSTGRES_DB_TEST = f"{Settings().POSTGRES_DB}_test"
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
    from app.src.core.database import Session, Base
    db = Session()
    Base.metadata.create_all(engine)
    print(f"The {POSTGRES_DB_TEST} ready")
    try:
        yield db
    finally:
        db.close()