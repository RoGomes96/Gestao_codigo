from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pfsw_gestao.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
