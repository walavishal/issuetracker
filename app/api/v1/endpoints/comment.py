from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.comment import CommentCreate, CommentOut
from app.services.comment_service import create_comment, get_comments_by_issue
from app.api.deps import get_db, get_current_user
from app.db.models.user import User

router = APIRouter()


@router.post("/issues/{issue_id}/comments", response_model=CommentOut)
def add_comment(
    issue_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_comment(
        db=db,
        user_id=current_user.id,
        issue_id=issue_id,
        content=payload.content
    )

@router.get("/issue/{issue_id}/comments", response_model=list[CommentOut])
def list_comments(issue_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_comments_by_issue(db, issue_id)