from databases import Database
from .config import settings

DATABASE_CONNECT = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

database = Database(DATABASE_CONNECT)
