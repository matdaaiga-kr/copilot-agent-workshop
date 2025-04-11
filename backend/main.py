import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, EmailStr

# Load environment variables
load_dotenv()

app = FastAPI()

# Pydantic models for request validation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr = None
    username: str = None
    profile_image: str = None

class PostCreate(BaseModel):
    content: str

class PostUpdate(BaseModel):
    content: str

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String, unique=True, index=True)
    profile_image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Follower(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    following_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Add a unique constraint to prevent duplicate follows
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='_follower_following_uc'),
    )

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Add a unique constraint to prevent duplicate likes
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='_user_post_like_uc'),
    )
    
    # Relationships
    user = relationship("User")
    post = relationship("Post")

Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication routes
@app.post("/auth/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and save user
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@app.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Retrieve user from database
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": existing_user.id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": existing_user.id})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# User routes
@app.get("/users/me")
def get_my_info(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve authenticated user's information
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"id": user.id, "email": user.email, "username": user.username, "profile_image": user.profile_image}}

@app.get("/users/{id}")
def get_user_profile(id: int, db: Session = Depends(get_db)):
    # Retrieve specific user's profile
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"id": user.id, "email": user.email, "username": user.username, "profile_image": user.profile_image}}

@app.put("/users/me")
def update_my_info(user_update: UserUpdate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Update authenticated user's information
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.email:
        user.email = user_update.email
    if user_update.username:
        user.username = user_update.username
    if user_update.profile_image:
        user.profile_image = user_update.profile_image
        
    db.commit()
    return {"message": "User updated successfully"}

@app.post("/users/{id}/follow")
def follow_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Check if the follow relationship already exists
    existing_follow = db.query(Follower).filter(
        Follower.follower_id == user_id, 
        Follower.following_id == id
    ).first()
    
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user")
        
    follow = Follower(follower_id=user_id, following_id=id)
    db.add(follow)
    db.commit()
    return {"message": f"Started following user {id}"}

@app.delete("/users/{id}/follow")
def unfollow_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Unfollow a user
    follow = db.query(Follower).filter(
        Follower.follower_id == user_id, 
        Follower.following_id == id
    ).first()
    
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
        
    db.delete(follow)
    db.commit()
    return {"message": f"Stopped following user {id}"}

# Post routes
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    # Retrieve all posts
    posts = db.query(Post).all()
    return {"posts": posts}

@app.post("/posts")
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Create a new post for the authenticated user
    new_post = Post(content=post.content, owner_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "post": new_post}

@app.get("/posts/{id}")
def get_post_detail(id: int, db: Session = Depends(get_db)):
    # Retrieve specific post details
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Delete a post
    post = db.query(Post).filter(Post.id == id, Post.owner_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    db.delete(post)
    db.commit()
    return {"message": f"Post {id} deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, post_update: PostUpdate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Update a post
    post = db.query(Post).filter(Post.id == id, Post.owner_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    post.content = post_update.content
    db.commit()
    return {"message": f"Post {id} updated successfully"}

# Comment routes
@app.get("/posts/{id}/comments")
def get_post_comments(id: int, db: Session = Depends(get_db)):
    # Retrieve comments for a specific post
    comments = db.query(Comment).filter(Comment.post_id == id).all()
    return {"comments": comments}

@app.post("/posts/{id}/comments")
def create_comment(id: int, comment: CommentCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Create a comment for a specific post
    new_comment = Comment(content=comment.content, post_id=id, owner_id=user_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": f"Comment added to post {id}", "comment": new_comment}

@app.delete("/comments/{id}")
def delete_comment(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Delete a comment
    comment = db.query(Comment).filter(Comment.id == id, Comment.owner_id == user_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    db.delete(comment)
    db.commit()
    return {"message": f"Comment {id} deleted successfully"}

@app.put("/comments/{id}")
def update_comment(id: int, comment_update: CommentUpdate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Update a comment
    comment = db.query(Comment).filter(Comment.id == id, Comment.owner_id == user_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    comment.content = comment_update.content
    db.commit()
    return {"message": f"Comment {id} updated successfully"}

# Like routes
@app.post("/posts/{id}/like")
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

@app.delete("/posts/{id}/like")
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

# Profile routes
@app.get("/profile")
def get_profile(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve profile information for the authenticated user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"profile": {"id": user.id, "email": user.email, "username": user.username, "profile_image": user.profile_image}}

@app.get("/profile/posts")
def get_my_posts(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve posts created by the authenticated user
    posts = db.query(Post).filter(Post.owner_id == user_id).all()
    return {"posts": posts}

@app.get("/profile/followers")
def get_followers(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve followers for the authenticated user
    followers = db.query(Follower).filter(Follower.following_id == user_id).all()
    follower_users = []
    for follow in followers:
        follower = db.query(User).filter(User.id == follow.follower_id).first()
        if follower:
            follower_users.append({
                "id": follower.id,
                "username": follower.username,
                "profile_image": follower.profile_image
            })
    return {"followers": follower_users}

@app.get("/profile/following")
def get_following(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve users the authenticated user is following
    following = db.query(Follower).filter(Follower.follower_id == user_id).all()
    following_users = []
    for follow in following:
        followed = db.query(User).filter(User.id == follow.following_id).first()
        if followed:
            following_users.append({
                "id": followed.id,
                "username": followed.username,
                "profile_image": followed.profile_image
            })
    return {"following": following_users}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Threads-like Application API",
        version="1.0.0",
        description="This is a Threads-like application backend API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi