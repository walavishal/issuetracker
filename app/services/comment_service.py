from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.comment import Comment
from app.db.models.issue import Issue
from app.db.models.user import User


def create_comment(db: Session, user_id: int, issue_id: int, content: str):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    comment = Comment(
        content=content,
        issue_id=issue_id,
        user_id=user_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments_by_issue(db: Session, issue_id: int):
    return db.query(Comment).filter(Comment.issue_id == issue_id).all()