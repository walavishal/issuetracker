from sqlalchemy.orm import Session
from app.db.models.issue import Issue
from fastapi import HTTPException
from app.services.user_service import get_user_or_404


def create_issue(db: Session, data: dict, project_id: int):
    issue = Issue(**data, project_id=project_id)
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def get_issues_by_project(db: Session, project_id: int, limit: int, offset: int):
    return (
        db.query(Issue)
        .filter(Issue.project_id == project_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_issues_by_project(db: Session, project_id: int):
    return db.query(Issue).filter(Issue.project_id == project_id).count()


def get_issue_by_id(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()


def update_issue_status(db: Session, issue: Issue, status):
    issue.status = status
    db.commit()
    db.refresh(issue)
    return issue

def assign_issue(db, issue, user_id):

    user = get_user_or_404(db, user_id)

    issue.assigned_to = user.id

    db.commit()
    db.refresh(issue)

    return issue