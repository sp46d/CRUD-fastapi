from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import select
from .. import schemas, models, oauth2
from ..database import SessionLocal

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    with SessionLocal() as session:
        post = session.get(models.Post, vote.post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post {vote.post_id} was not found")
    
        found_vote = session.scalar(
            select(models.Vote)
            .where(models.Vote.post_id == vote.post_id,
                   models.Vote.user_id == current_user.id))
    
        if vote.dir == 1:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"user {current_user.id} already voted on post {vote.post_id}")
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            session.add(new_vote)
            session.commit()

            return {"message": "vote is successfully added"}
            
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"user {current_user.id} did not vote on post {vote.post_id}, so cannot unvote post {vote.post_id}")
            session.delete(found_vote)
            session.commit()
            
            return {"message": "vote is successfully deleted"}
    
    
# @router.get("/{id}", response_model=schemas.VoteOut)
# def get_votes(id: int,
#               db: Session = Depends(get_db),
#               current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
#     query = db.query(models.Post, models.Vote)\
#         .outerjoin(models.Vote, models.Post.id == models.Vote.post_id)\
#         .group_by(models.Post.id).count()
        
        
        