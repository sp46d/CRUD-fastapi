from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_engine(f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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