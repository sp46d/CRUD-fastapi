from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def vote(vote: schemas.Vote,
         db: Session = Depends(get_db),
         current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()
    
    post_voted = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post_voted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {vote.post_id} was not found")
    
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        post_voted.likes += 1
    else:
        if vote_found:
            vote_query.delete(synchronize_session=False)
            post_voted.likes -= 1
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} did not vote on post {vote.post_id}, so cannot unvote post {vote.post_id}")
            
    db.commit()
    
    return post_voted