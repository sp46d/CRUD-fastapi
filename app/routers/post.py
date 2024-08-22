from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import Optional
from sqlalchemy import select, update, func
from .. import models, schemas, oauth2
from ..database import SessionLocal



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get('/', response_model=List[schemas.Post])
@router.get('/')
def get_posts(current_user: schemas.UserOut = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str]= ""):
    
    # with SessionLocal() as session:
    #     posts = session.scalars(
    #         select(models.Post)
    #         .where(models.Post.title.ilike(f'%{search}%'))
    #         .offset(skip)
    #         .limit(limit)).all()
    
    with SessionLocal() as session:
        vote_count = func.count(models.Vote.post_id).label("votes")
        q = (select(models.Post, models.User, vote_count)
             .join(models.Post.votes, isouter=True)
             .join(models.Post.owner)
             .group_by(models.Post, models.User))
        posts = session.execute(q).mappings().all()
    return posts
            
    # posts = db.query(models.Post).all()
    # result = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
    #     .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
    #     .group_by(models.Post.id).first()
    
    # result = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).all()
    



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    with SessionLocal() as session:
        new_post = models.Post(owner_id=current_user.id, **post.model_dump())
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, 
             current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    with SessionLocal() as session:
        post = session.get(models.Post, id)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    with SessionLocal() as session:
        post = session.get(models.Post, id)
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")
            
        if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authorized to perform requested action")
        
        session.delete(post)
        session.commit()
            
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, 
                post: schemas.PostCreate, 
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    with SessionLocal() as session:
        old_post = session.get(models.Post, id)

        if not old_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")
            
        if old_post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authorized to perform requested action")
    
        session.execute(update(models.Post)
                        .where(models.Post.id == id)
                        .values(**post.model_dump())
                        .execution_options(synchronize_session=False))
        session.commit()
        session.refresh(old_post)

    return old_post