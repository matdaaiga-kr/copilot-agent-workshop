import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.openapi.utils import get_openapi

# Load environment variables
load_dotenv()

app = FastAPI()

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
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
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
def signup(email: str, password: str, db: SessionLocal = Depends(get_db)):
    # Check if user already exists
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and save user
    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@app.post("/auth/login")
def login(email: str, password: str, db: SessionLocal = Depends(get_db)):
    # Retrieve user from database
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/auth/logout")
def logout():
    # Invalidate the token (implementation depends on token storage strategy)
    return {"message": "Logged out successfully"}

# User routes
@app.get("/users/me", dependencies=[Depends(verify_token)])
def get_my_info(db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Retrieve authenticated user's information
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"email": user.email}}

@app.get("/users/{id}")
def get_user_profile(id: int, db: SessionLocal = Depends(get_db)):
    # Retrieve specific user's profile
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"email": user.email}}

@app.put("/users/me", dependencies=[Depends(verify_token)])
def update_my_info(email: str, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Update authenticated user's information
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = email
    db.commit()
    return {"message": "User updated successfully"}

@app.post("/users/{id}/follow", dependencies=[Depends(verify_token)])
def follow_user(id: int, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Follow a user
    follow = Follower(follower=username, following=id)
    db.add(follow)
    db.commit()
    return {"message": f"Started following user {id}"}

@app.delete("/users/{id}/follow", dependencies=[Depends(verify_token)])
def unfollow_user(id: int, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Unfollow a user
    follow = db.query(Follower).filter(Follower.follower == username, Follower.following == id).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
    db.delete(follow)
    db.commit()
    return {"message": f"Stopped following user {id}"}

# Post routes
@app.get("/posts")
def get_all_posts(db: SessionLocal = Depends(get_db)):
    # Retrieve all posts
    posts = db.query(Post).all()
    return {"posts": posts}

@app.post("/posts", dependencies=[Depends(verify_token)])
def create_post(content: str, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Create a new post for the authenticated user
    new_post = Post(content=content, owner=username)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "post": new_post}

@app.get("/posts/{id}")
def get_post_detail(id: int, db: SessionLocal = Depends(get_db)):
    # Retrieve specific post details
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}

@app.delete("/posts/{id}", dependencies=[Depends(verify_token)])
def delete_post(id: int, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Delete a post
    post = db.query(Post).filter(Post.id == id, Post.owner == username).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    db.delete(post)
    db.commit()
    return {"message": f"Post {id} deleted successfully"}

@app.put("/posts/{id}", dependencies=[Depends(verify_token)])
def update_post(id: int, content: str, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Update a post
    post = db.query(Post).filter(Post.id == id, Post.owner == username).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    post.content = content
    db.commit()
    return {"message": f"Post {id} updated successfully"}

# Comment routes
@app.get("/posts/{id}/comments")
def get_post_comments(id: int, db: SessionLocal = Depends(get_db)):
    # Retrieve comments for a specific post
    comments = db.query(Comment).filter(Comment.post_id == id).all()
    return {"comments": comments}

@app.post("/posts/{id}/comments", dependencies=[Depends(verify_token)])
def create_comment(id: int, content: str, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Create a comment for a specific post
    comment = Comment(content=content, post_id=id, owner=username)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": f"Comment added to post {id}", "comment": comment}

@app.delete("/comments/{id}", dependencies=[Depends(verify_token)])
def delete_comment(id: int, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Delete a comment
    comment = db.query(Comment).filter(Comment.id == id, Comment.owner == username).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    db.delete(comment)
    db.commit()
    return {"message": f"Comment {id} deleted successfully"}

@app.put("/comments/{id}", dependencies=[Depends(verify_token)])
def update_comment(id: int, content: str, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Update a comment
    comment = db.query(Comment).filter(Comment.id == id, Comment.owner == username).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    comment.content = content
    db.commit()
    return {"message": f"Comment {id} updated successfully"}

# Like routes
@app.post("/posts/{id}/like", dependencies=[Depends(verify_token)])
def like_post(id: int, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Like a post
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes += 1
    db.commit()
    return {"message": f"Post {id} liked successfully"}

@app.delete("/posts/{id}/like", dependencies=[Depends(verify_token)])
def unlike_post(id: int, db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Unlike a post
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes -= 1
    db.commit()
    return {"message": f"Post {id} unliked successfully"}

# Profile routes
@app.get("/profile", dependencies=[Depends(verify_token)])
def get_profile(db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Retrieve profile information for the authenticated user
    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"profile": {"email": user.email}}

@app.get("/profile/posts", dependencies=[Depends(verify_token)])
def get_my_posts(db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Retrieve posts created by the authenticated user
    posts = db.query(Post).filter(Post.owner == username).all()
    return {"posts": posts}

@app.get("/profile/followers", dependencies=[Depends(verify_token)])
def get_followers(db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Retrieve followers for the authenticated user
    followers = db.query(Follower).filter(Follower.following == username).all()
    return {"followers": followers}

@app.get("/profile/following", dependencies=[Depends(verify_token)])
def get_following(db: SessionLocal = Depends(get_db), username: str = Depends(verify_token)):
    # Retrieve users the authenticated user is following
    following = db.query(Follower).filter(Follower.follower == username).all()
    return {"following": following}

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