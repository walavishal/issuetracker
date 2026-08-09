import json

from openai import OpenAI
from sqlalchemy.orm import Session
from app.db.models.project import Project
from app.core.config import settings
from app.db.models.user import User
from app.db.models.issue import Issue

from app.services.issue_service import (
    get_issue_by_id,
    assign_issue
)
from app.services.project_service import (
    create_project,
    update_project,
    delete_project
)
from app.services.issue_service import (
    create_issue,
    get_issues_by_project,
    update_issue_status,
    assign_issue
)

# -----------------------------
# TOOL FUNCTIONS
# -----------------------------

def find_user_by_email(db: Session, email: str):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name
    }


def assign_issue_tool(
    db: Session,
    issue_id: int,
    user_id: int
):
    issue = get_issue_by_id(db, issue_id)

    if not issue:
        return {
            "success": False,
            "message": "Issue not found"
        }

    updated_issue = assign_issue(
        db,
        issue,
        user_id
    )

    return {
        "success": True,
        "issue_id": updated_issue.id,
        "assigned_to": updated_issue.assigned_to
    }


def create_project_tool(db: Session, user_id: int, name: str, description: str | None = None):
    project = create_project(
        db=db,
        user_id=user_id,
        name=name,
        description=description
    )

    return {
        "success": True,
        "project_id": project.id,
        "name": project.name
    }


def update_project_tool(db: Session, project_id: int, data: dict):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"success": False, "message": "Project not found"}

    update_project(db, project, data)

    db.commit()
    db.refresh(project)

    return {
        "success": True,
        "project_id": project.id
    }

def delete_project_tool(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        return {"success": False, "message": "Project not found"}

    delete_project(db, project)

    return {
        "success": True,
        "message": "Project deleted"
    }

def create_issue_tool(
    db: Session,
    project_id: int,
    title: str,
    description: str,
    status: str = "OPEN"
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        return {
            "success": False,
            "message": f"Project {project_id} not found"
        }

    issue = create_issue(
        db=db,
        data={
            "title": title,
            "description": description,
            "status": status
        },
        project_id=project_id
    )

    return {
        "success": True,
        "issue_id": issue.id,
        "project_id": project_id
    }


def get_issues_tool(db: Session, project_id: int, limit: int = 10, offset: int = 0):
    issues = get_issues_by_project(db, project_id, limit, offset)

    return {
        "success": True,
        "issues": [
            {
                "id": i.id,
                "title": i.title,
                "status": i.status
            }
            for i in issues
        ]
    }

def update_issue_status_tool(db: Session, issue_id: int, status: str):
    issue = get_issue_by_id(db, issue_id)

    if not issue:
        return {"success": False, "message": "Issue not found"}

    updated = update_issue_status(db, issue, status)

    return {
        "success": True,
        "issue_id": updated.id,
        "status": updated.status
    }

def create_issue_with_ai_tool(
    db: Session,
    project_id: int,
    user_description: str,
    assign_to: int | None = None
):
    from app.services.ai_service import generate_issue_summary
    # Step 1: generate structured issue using LLM
    summary = generate_issue_summary(user_description)

    # Step 2: create issue in DB
    issue = create_issue(
        db=db,
        data={
            "title": summary.title,
            "description": summary.description,
            "status": "open"
        },
        project_id=project_id
    )

    result = {
        "success": True,
        "issue_id": issue.id,
        "project_id": project_id,
        "title": issue.title
    }

    # Step 3: optional assignment
    if assign_to:
        updated = assign_issue(db, issue, assign_to)
        result["assigned_to"] = updated.assigned_to

    return result


def find_project_by_name_tool(
    db: Session,
    name: str
):
    project = (
        db.query(Project)
        .filter(Project.name.ilike(name))
        .first()
    )

    if not project:
        return {
            "success": False,
            "message": "Project not found"
        }

    return {
        "success": True,
        "project_id": project.id,
        "name": project.name,
        "description": project.description
    }
def get_project_tool(
    db: Session,
    project_id: int
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        return {
            "success": False,
            "message": "Project not found"
        }

    return {
        "success": True,
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description
        }
    }

def get_user_issues_tool_or_get_current_user_issues_tool(
    db: Session,
    user_id: int
):
    issues = (
        db.query(Issue)
        .filter(Issue.assigned_to == user_id)
        .all()
    )

    return {
        "success": True,
        "issues": [
            {
                "id": issue.id,
                "title": issue.title,
                "status": issue.status,
                "project_id": issue.project_id
            }
            for issue in issues
        ]
    }

def list_projects_tool(
    db: Session,
    current_user_id: int
):
    projects = (
        db.query(Project)
        .filter(Project.created_by == current_user_id)
        .all()
    )

    return {
        "success": True,
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description
            }
            for project in projects
        ]
    }
TOOL_FUNCTIONS = {
    "find_user_by_email": find_user_by_email,
    "create_issue_tool": create_issue_tool,
    "get_issues_tool": get_issues_tool,
    "update_issue_status_tool": update_issue_status_tool,
    "assign_issue_tool": assign_issue_tool,
    "create_project_tool": create_project_tool,
    "update_project_tool": update_project_tool,
    "delete_project_tool": delete_project_tool,
    "create_issue_with_ai_tool": create_issue_with_ai_tool,
    "find_project_by_name_tool": find_project_by_name_tool,
    "get_project_tool": get_project_tool,
    "get_user_issues_tool_or_get_current_user_issues_tool": get_user_issues_tool_or_get_current_user_issues_tool,
    "list_projects_tool": list_projects_tool,
}


#********************************************************************

# def find_user_by_email(
#     db: Session,
#     email: str
# ):
#     user = (
#         db.query(User)
#         .filter(User.email == email)
#         .first()
#     )

#     if not user:
#         return {
#             "success": False,
#             "message": "User not found"
#         }

#     return {
#         "success": True,
#         "user": {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "is_active": user.is_active
#         }
#     }
# def get_user_tool(
#     db: Session,
#     user_id: int
# ):
#     user = (
#         db.query(User)
#         .filter(User.id == user_id)
#         .first()
#     )

#     if not user:
#         return {
#             "success": False,
#             "message": "User not found"
#         }

#     return {
#         "success": True,
#         "user": {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "is_active": user.is_active
#         }
#     }
# def get_current_user_tool(
#     db: Session,
#     current_user_id: int
# ):
#     user = (
#         db.query(User)
#         .filter(User.id == current_user_id)
#         .first()
#     )

#     if not user:
#         return {
#             "success": False,
#             "message": "User not found"
#         }

#     return {
#         "success": True,
#         "user": {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email
#         }
#     }

# def search_users_tool(
#     db: Session,
#     query: str
# ):
#     users = (
#         db.query(User)
#         .filter(User.email.ilike(f"%{query}%"))
#         .all()
#     )

#     return {
#         "success": True,
#         "users": [
#             {
#                 "id": user.id,
#                 "name": user.name,
#                 "email": user.email
#             }
#             for user in users
#         ]
#     }

# TOOL_FUNCTIONS = {
#     "find_user_by_email": find_user_by_email,
#     "get_user_tool": get_user_tool,
#     "get_current_user_tool": get_current_user_tool,
#     "search_users_tool": search_users_tool,
# }