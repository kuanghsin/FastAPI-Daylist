from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import hash_password, verify_csrf, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import Credentials

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", dependencies=[Depends(verify_csrf)])
def register(data: Credentials, request: Request, db: Session = Depends(get_db)):
    user = User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="帳號已存在") from None
    db.refresh(user)
    request.session.clear()
    request.session["user_id"] = user.id
    return {"username": user.username}


@router.post("/login", dependencies=[Depends(verify_csrf)])
def login(data: Credentials, request: Request, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == data.username))
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")
    request.session.clear()
    request.session["user_id"] = user.id
    return {"username": user.username}


@router.post("/logout", dependencies=[Depends(verify_csrf)])
def logout(request: Request):
    request.session.clear()
    return {"message": "已登出"}
