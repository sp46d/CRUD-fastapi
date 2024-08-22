from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


# READ documentation to understand OAuth2PasswordRequestForm
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    
    with database.SessionLocal() as session:
        user = session.scalar(
                select(models.User)
                .where(models.User.email == user_credentials.username))
    
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid credentials")
            
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid credentials")
            
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        
    return {"access_token": access_token, "token_type": "bearer"}
