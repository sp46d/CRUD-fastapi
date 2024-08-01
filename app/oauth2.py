import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: str | None = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        
        return token_data
    
    except InvalidTokenError:
        raise credentials_exception

    
def get_current_user(access_token: str = Depends(oauth2_scheme),
                     db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(access_token ,credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
    
    