from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.models import Post, Like
from ..models.schemas import PostCreate, PostUpdate, PostResponse
from ..security.auth import verify_token

router = APIRouter(tags=["Posts"])

@router.get("", response_model=dict)
def get_all_posts(db: Session = Depends(get_db)):
    # Retrieve all posts
    posts = db.query(Post).all()
    return {"posts": posts}

@router.post("", response_model=dict)
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Create a new post for the authenticated user
    new_post = Post(content=post.content, owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "post": new_post}

@router.get("/{id}", response_model=dict)
def get_post_detail(id: int, db: Session = Depends(get_db)):
    # Retrieve specific post details
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}

@router.delete("/{id}", response_model=dict)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Delete a post
    post = db.query(Post).filter(Post.id == id, Post.owner_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    db.delete(post)
    db.commit()
    return {"message": f"Post {id} deleted successfully"}

@router.put("/{id}", response_model=dict)
def update_post(id: int, post_update: PostUpdate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Update a post
    post = db.query(Post).filter(Post.id == id, Post.owner_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    post.content = post_update.content
    db.commit()
    return {"message": f"Post {id} updated successfully"}

@router.post("/{id}/like", response_model=dict)
def like_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Check if post exists
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")
    
    # Create new like
    like = Like(user_id=user_id, post_id=id)
    db.add(like)
    
    # Update post likes count
    post.likes += 1
    
    db.commit()
    return {"message": f"Post {id} liked successfully"}

@router.delete("/{id}/like", response_model=dict)
def unlike_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Check if post exists
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if liked
    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == id
    ).first()
    
    if not existing_like:
        raise HTTPException(status_code=404, detail="Post not liked")
    
    # Delete like
    db.delete(existing_like)
    
    # Update post likes count
    if post.likes > 0:
        post.likes -= 1
    
    db.commit()
    return {"message": f"Post {id} unliked successfully"}