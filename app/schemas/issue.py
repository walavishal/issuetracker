from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.db.enums.issue import IssueStatus, IssuePriority


class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: IssuePriority = IssuePriority.MEDIUM


class IssueOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: IssueStatus
    priority: IssuePriority
    project_id: int
    assigned_to: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


class IssueStatusUpdate(BaseModel):
    status: IssueStatus


class IssueAssign(BaseModel):
    user_id: int