from sqlalchemy_utils import create_database, database_exists, drop_database
import os

POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tournament")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
DB_URL_BASE: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432"
DB_URL: str = f"{DB_URL_BASE}/{POSTGRES_DB}"

if __name__ == "__main__":
    if not database_exists(DB_URL):
        print(f"Criando database {DB_URL}")
        create_database(DB_URL)
