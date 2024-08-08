from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: start the session with a context manager, instead of the function below
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password='Qkrtkdgur!',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
    
#     except Exception as error:
#         print("Connecting to database failed.")
#         print("The error was:", error)
#         time.sleep(2)        