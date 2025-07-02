from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, utils, auth

router = APIRouter(tags=["Ops User"])

@router.post("/ops/login", response_model=schemas.Token)
def ops_login(user_data: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email, models.User.role == "ops").first()
    if not user or not utils.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = utils.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
