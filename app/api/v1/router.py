from fastapi import APIRouter
from app.api.v1.endpoints import auth,user,project,issue, comment

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)


api_router.include_router(
    user.router,
    prefix="/users",
    tags=["User"]
)

api_router.include_router(
    project.router,
    prefix="/projects", 
    tags=["Projects"]
)

api_router.include_router(
    issue.router,
    prefix="/issues", 
    tags=["Issues"]
)

api_router.include_router(
    comment.router,
    prefix="/comments", 
    tags=["Comments"]
)

