from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_exponential
from shared.config.settings import settings

class Database:
    def __init__(self, url: str = settings.DATABASE_URL):
        self.engine = create_engine(
            url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_db(self):
        try:
            db = self.SessionLocal()
            yield db
        except OperationalError:
            raise
        finally:
            db.close()

db = Database()
get_db = db.get_db