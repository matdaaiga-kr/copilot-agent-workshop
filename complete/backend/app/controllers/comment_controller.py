from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate

def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    """특정 게시글의 모든 댓글 조회"""
    # 게시글 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: CommentCreate, post_id: int, user_id: int):
    """새 댓글 작성"""
    # 게시글 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    
    db_comment = Comment(
        content=comment.content,
        post_id=post_id,
        owner_id=user_id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    """ID로 특정 댓글 조회"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다."
        )
    return comment

def verify_comment_post(db: Session, comment_id: int, post_id: int):
    """댓글이 해당 게시물에 속하는지 확인"""
    comment = get_comment(db, comment_id)
    if comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 게시물에 속하는 댓글이 아닙니다."
        )
    return comment

def update_comment(db: Session, comment_id: int, comment: CommentUpdate, user_id: int, post_id: int = None):
    """댓글 수정"""
    db_comment = get_comment(db, comment_id)
    
    # 해당 게시물의 댓글인지 확인
    if post_id is not None:
        verify_comment_post(db, comment_id, post_id)
    
    # 댓글 작성자만 수정 가능
    if db_comment.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 댓글을 수정할 권한이 없습니다."
        )
    
    db_comment.content = comment.content
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int, user_id: int, post_id: int = None):
    """댓글 삭제"""
    db_comment = get_comment(db, comment_id)
    
    # 해당 게시물의 댓글인지 확인
    if post_id is not None:
        verify_comment_post(db, comment_id, post_id)
    
    # 댓글 작성자만 삭제 가능
    if db_comment.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 댓글을 삭제할 권한이 없습니다."
        )
    
    db.delete(db_comment)
    db.commit()
    
    return {"message": "댓글이 성공적으로 삭제되었습니다."}