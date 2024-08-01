from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
              current_user: schemas.UserOut = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str]= ""):
    print(search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, 
             db: Session = Depends(get_db),
             current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, 
                post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    if post_query.first().owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()