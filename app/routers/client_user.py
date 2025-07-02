from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app import models, schemas, utils, auth
from fastapi import BackgroundTasks

from app.database import SessionLocal
from app.email_utils import send_verification_email
import asyncio
router = APIRouter(tags=["Client User"])

@router.post("/client/signup", status_code=201)
def client_signup(user_data: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = utils.hash_password(user_data.password)
    new_user = models.User(email=user_data.email, password=hashed_pw, role="client")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate fake encrypted URL for now
    encrypted_url = utils.create_access_token({"sub": new_user.email})
    # asyncio.create_task(send_verification_email(new_user.email, encrypted_url))
    BackgroundTasks.add_task(send_verification_email, new_user.email)
    return {
        "message": "User created successfully. Verification email sent.",
        "verify-link": f"http://localhost:8000/client/verify-email?token={encrypted_url}"
    }

@router.post("/client/login", response_model=schemas.Token)
def client_login(user_data: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email, models.User.role == "client").first()
    if not user or not utils.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email")
    
    token = utils.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/client/verify-email")
def verify_email(token: str, db: Session = Depends(auth.get_db)):
    try:
        payload = utils.decode_token(token)
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email, models.User.role == "client").first()
        if not user:
            raise HTTPException(404, detail="User not found")
        user.is_verified = True
        db.commit()
        return {"message": "Email verified successfully. You can now login."}
    except:
        raise HTTPException(400, detail="Invalid or expired token")
