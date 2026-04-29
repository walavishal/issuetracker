from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.services.project_service import (
    create_project,
    get_all_projects,
    get_project_by_id,
    update_project,
    delete_project
)
from app.utils.response import success_response, error_response
from app.db.models.user import User
from app.services.project_service import (
    get_user_projects,
    count_user_projects
)
from app.api.deps import get_pagination
from app.schemas.common import PaginationParams

router = APIRouter()


@router.post("/")
def create_project_api(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = create_project(
        db,
        user_id=current_user.id,
        name=payload.name,
        description=payload.description
    )

    return success_response(
        message="Project created",
        data=ProjectOut.model_validate(project).model_dump(),
        status_code=status.HTTP_201_CREATED
    )


@router.get("/")
def get_projects_api(
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects = get_user_projects(
        db,
        user_id=current_user.id,
        limit=pagination.limit,
        offset=pagination.offset
    )

    total = count_user_projects(db, user_id=current_user.id)

    return success_response(
        message="Projects fetched",
        data={
            "items": [
                ProjectOut.model_validate(p).model_dump()
                for p in projects
            ],
            "pagination": {
                "total": total,
                "limit": pagination.limit,
                "offset": pagination.offset
            }
        }
    )


@router.get("/{project_id}")
def get_project_api(project_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    project = get_project_by_id(db, project_id)

    if not project:
        return error_response("Project not found", status_code=404)

    return success_response(
        message="Project details",
        data=ProjectOut.model_validate(project).model_dump()
    )


@router.put("/{project_id}")
def update_project_api(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = get_project_by_id(db, project_id)

    if not project:
        return error_response("Project not found", status_code=404)

    updated = update_project(db, project, payload.model_dump(exclude_unset=True))

    return success_response(
        message="Project updated",
        data=ProjectOut.model_validate(updated).model_dump()
    )


@router.delete("/{project_id}")
def delete_project_api(project_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    project = get_project_by_id(db, project_id)

    if not project:
        return error_response("Project not found", status_code=404)

    delete_project(db, project)

    return success_response(
        message="Project deleted",
        data=None
    )