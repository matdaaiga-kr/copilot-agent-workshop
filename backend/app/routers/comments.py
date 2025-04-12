from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.models import Comment
from ..models.schemas import CommentCreate, CommentUpdate
from ..security.auth import verify_token

router = APIRouter(tags=["Comments"])

@router.get("/posts/{post_id}/comments", response_model=dict)
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    # Retrieve comments for a specific post
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return {"comments": comments}

@router.post("/posts/{post_id}/comments", response_model=dict)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Create a comment for a specific post
    new_comment = Comment(content=comment.content, post_id=post_id, owner_id=user_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": f"Comment added to post {post_id}", "comment": new_comment}

@router.delete("/comments/{id}", response_model=dict)
def delete_comment(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Delete a comment
    comment = db.query(Comment).filter(Comment.id == id, Comment.owner_id == user_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    db.delete(comment)
    db.commit()
    return {"message": f"Comment {id} deleted successfully"}

@router.put("/comments/{id}", response_model=dict)
def update_comment(id: int, comment_update: CommentUpdate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Update a comment
    comment = db.query(Comment).filter(Comment.id == id, Comment.owner_id == user_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    comment.content = comment_update.content
    db.commit()
    return {"message": f"Comment {id} updated successfully"}