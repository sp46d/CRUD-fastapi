from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.put("/{post_id}", response_model=schemas.Post)
def vote(post_id: int,
         db: Session = Depends(get_db),
         current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    

    post_voted = db.query(models.Post).filter(models.Post.id == post_id)
    if post_voted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} was not found")
    
    post_voted.first().likes += 1
    
    post_user_id = int(str(post_id) + str(current_user.id))
    new_vote = models.Vote(post_user_id=post_user_id, post_id=post_id, user_id=current_user.id)
    
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    
    
    return post_voted.first()