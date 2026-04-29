from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.user import UserOut, UpdateProfile, ChangePassword
from app.services.user_service import update_user_profile, change_user_password
from app.utils.response import success_response, error_response
from app.db.models.user import User

router = APIRouter()


# Get Profile
@router.get("/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


# Update Profile
@router.put("/profile")
def update_profile(
    payload: UpdateProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = update_user_profile(db, current_user, payload.name)

    return success_response(
        message="Profile updated successfully",
        data=UserOut.model_validate(user).model_dump(),
        status_code=status.HTTP_200_OK
    )


# Change Password
@router.put("/change-password")
def change_password(
    payload: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = change_user_password(
        db,
        current_user,
        payload.current_password,
        payload.new_password
    )

    if not success:
        return error_response(
            message="Current password is incorrect",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return success_response(
        message="Password updated successfully",
        data=None,
        status_code=status.HTTP_200_OK
    )