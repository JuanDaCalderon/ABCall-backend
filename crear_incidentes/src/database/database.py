import os
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import create_database, database_exists

env_file = find_dotenv('.env.incidentes')
loaded = load_dotenv(env_file)

username = os.environ.get("DB_USER") if os.environ.get(
    "DB_USER") is not None and os.environ.get("DB_USER") != "" else "postgres"
password = os.environ.get("DB_PASSWORD") if os.environ.get(
    "DB_PASSWORD") is not None and os.environ.get("DB_PASSWORD") != "" else "postgres"
host = os.environ.get("DB_HOST") if os.environ.get(
    "DB_HOST") is not None and os.environ.get("DB_HOST") != "" else "localhost"
database = os.environ.get("DB_NAME") if os.environ.get(
    "DB_NAME") is not None and os.environ.get("DB_NAME") != "" else "postgres"
port = os.environ.get("DB_PORT") if os.environ.get(
    "DB_PORT") is not None and os.environ.get("DB_PORT") != "" else "5432"

print('********************************************************************************************************')
print('DB_USER->', username, '   '
      'DB_PASSWORD->', password, '   '
      'DB_HOST->', host, '   '
      'DB_NAME->', database, '   '
      'DB_PORT->', port)
print('********************************************************************************************************')

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=username,
    password=password,
    host=host,
    database=database,
    port=port,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
