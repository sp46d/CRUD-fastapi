from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def vote(body: schemas.Vote,
         db: Session = Depends(get_db),
         current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    post_voted = db.query(models.Post).filter(models.Post.id == body.post_id).first()
    if post_voted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {body.post_id} was not found")
    
    vote_exist = db.query(models.Vote)\
            .filter(models.Vote.post_id == body.post_id, models.Vote.user_id == current_user.id)\
        
    if vote_exist.first():
        vote_exist.delete(synchronize_session=False)
        post_voted.likes -= 1

    else:
        new_vote = models.Vote(post_id=body.post_id, user_id=current_user.id)
        db.add(new_vote)
        post_voted.likes += 1
        
    db.commit()
    # db.refresh(new_vote)
        
    return post_voted