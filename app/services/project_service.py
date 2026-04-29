from sqlalchemy.orm import Session
from app.db.models.project import Project
from fastapi import HTTPException

def create_project(db: Session, user_id: int, name: str, description: str | None):
    project = Project(
        name=name,
        description=description,
        created_by=user_id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_all_projects(db: Session):
    return db.query(Project).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def update_project(db: Session, project: Project, data: dict):
    for key, value in data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project):
    db.delete(project)
    db.commit()



def get_user_projects(db: Session, user_id: int, limit: int, offset: int):
    return (
        db.query(Project)
        .filter(Project.created_by == user_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_user_projects(db: Session, user_id: int):
    return (
        db.query(Project)
        .filter(Project.created_by == user_id)
        .count()
    )


def get_user_project(db, project_id, user_id):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == user_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found or not authorized"
        )

    return project