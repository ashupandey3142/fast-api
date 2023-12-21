from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from day5.project.config.db import LocalSession
from day5.project.schema.index import Token
from day5.project.service.service import authenticate_user, create_access_token

def login_for_access_token(form_data: dict, db: Session = Depends(LocalSession)):
    user = authenticate_user(db, form_data["username"], form_data["password"])
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expire = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MIN))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expire
    )
    return Token(access_token=access_token, token_type="Bearer")
