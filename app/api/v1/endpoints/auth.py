from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.core.security import create_access_token, create_refresh_token, decode_access_token
from app.utils.response import success_response, error_response
from fastapi import status
router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        return error_response("Email already registered", 400)

    new_user = create_user(
        db=db,
        email=user.email,
        name=user.name,
        password=user.password
    )

    return success_response(
        message="User created successfully",
        data={},
        status_code=status.HTTP_201_CREATED
    )

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        return error_response(
            "Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    payload = {
        "sub": str(db_user.id),
        "email": db_user.email
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return success_response(
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": UserOut.model_validate(db_user).model_dump()
        },
        status_code=status.HTTP_200_OK
    )



@router.post("/refresh")
def refresh_token(refresh_token: str):
    
    payload = decode_access_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        return error_response(
            "Invalid refresh token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    new_access_token = create_access_token({
        "sub": payload.get("sub"),
        "email": payload.get("email")
    })

    return success_response(
        message="Token refreshed",
        data={
            "access_token": new_access_token,
        },
        status_code=status.HTTP_200_OK
    )