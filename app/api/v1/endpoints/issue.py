from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_pagination
from app.schemas.issue import (
    IssueCreate, IssueOut, IssueStatusUpdate, IssueAssign
)
from app.schemas.common import PaginationParams
from app.services.issue_service import *
from app.utils.response import success_response, error_response
from app.db.models.user import User

router = APIRouter()


@router.post("/{project_id}")
def create_issue_api(
    project_id: int,
    payload: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = create_issue(db, payload.model_dump(), project_id)

    return success_response(
        message="Issue created",
        data=IssueOut.model_validate(issue).model_dump()
    )

@router.get("/projects/{project_id}")
def get_project_issues_api(
    project_id: int,
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issues = get_issues_by_project(
        db, project_id, pagination.limit, pagination.offset
    )

    total = count_issues_by_project(db, project_id)

    return success_response(
        message="Issues fetched",
        data={
            "items": [
                IssueOut.model_validate(i).model_dump()
                for i in issues
            ],
            "pagination": {
                "total": total,
                "limit": pagination.limit,
                "offset": pagination.offset
            }
        }
    )


@router.get("/{issue_id}")
def get_issue_api(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = get_issue_by_id(db, issue_id)

    if not issue:
        return error_response("Issue not found", 404)

    return success_response(
        message="Issue details",
        data=IssueOut.model_validate(issue).model_dump()
    )


@router.put("/{issue_id}/status")
def update_status_api(
    issue_id: int,
    payload: IssueStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = get_issue_by_id(db, issue_id)

    if not issue:
        return error_response("Issue not found", 404)

    updated = update_issue_status(db, issue, payload.status)

    return success_response(
        message="Status updated",
        data=IssueOut.model_validate(updated).model_dump()
    )

@router.put("/{issue_id}/assign")
def assign_issue_api(
    issue_id: int,
    payload: IssueAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = get_issue_by_id(db, issue_id)

    if not issue:
        return error_response("Issue not found", 404)

    updated = assign_issue(db, issue, payload.user_id)

    return success_response(
        message="Issue assigned",
        data=IssueOut.model_validate(updated).model_dump()
    )
