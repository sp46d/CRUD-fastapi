from fastapi import status, HTTPException, APIRouter
from .. import schemas, models, utils
from ..database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    with SessionLocal() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int):
    
    with SessionLocal() as session:
        user = session.get(models.User, id)
    
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user with id: {id} does not exist")
            
    return user