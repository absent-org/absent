from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read("config.ini")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{cfg['PostgreSQL']['user']}:{cfg['PostgreSQL']['password']}@127.0.0.1/{cfg['PostgreSQL']['name']}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()