from pydantic import BaseModel, Field


class AIssueSummaryResponse(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=10)
