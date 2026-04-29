from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.db.enums.issue import IssueStatus, IssuePriority
from sqlalchemy.orm import relationship

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)

    status = Column(Enum(IssueStatus), default=IssueStatus.OPEN, nullable=False)
    priority = Column(Enum(IssuePriority), default=IssuePriority.MEDIUM, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    project = relationship("Project", back_populates="issues")  
    comments = relationship("Comment", back_populates="issue", cascade="all, delete")