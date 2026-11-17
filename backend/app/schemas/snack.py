from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from app.models import SnackCategory
from app.services.snack_status import SnackStatus


class SnackBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: SnackCategory
    quantity: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)

    @field_validator('name')
    @classmethod
    def name_trim(cls, v: str) -> str:
        return v.strip()


class SnackCreate(SnackBase):
    pass


class SnackUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[SnackCategory] = None
    low_stock_threshold: Optional[int] = Field(None, ge=0)

    @field_validator('name')
    @classmethod
    def name_trim(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip()
        return v


class SnackResponse(BaseModel):
    id: str
    name: str
    category: SnackCategory
    quantity: int
    low_stock_threshold: int
    status: SnackStatus
    vote_count: int
    voted_by_me: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class SnackListResponse(BaseModel):
    items: list[SnackResponse]
    total: int
    page: int
    page_size: int
    pages: int


class SnackSummary(BaseModel):
    id: Optional[str]
    name: Optional[str]
    category: Optional[SnackCategory]
    vote_count: int
    quantity: int
    status: SnackStatus


class SummaryResponse(BaseModel):
    stocked: int
    running_low: int
    gone: int
    total: int
    snack_of_the_week: Optional[SnackSummary]


class SnackQueryParams(BaseModel):
    category: Optional[SnackCategory] = None
    status: Optional[SnackStatus] = None
    q: Optional[str] = Field(None, max_length=255)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=50)
    sort_by: Literal["name", "quantity", "votes", "created_at"] = "name"
    order: Literal["asc", "desc"] = "asc"


class ConsumeRequest(BaseModel):
    amount: int = Field(..., ge=1, le=100)


class RestockRequest(BaseModel):
    amount: int = Field(..., ge=1, le=10000)


class VoteResponse(BaseModel):
    vote_count: int
    voted_by_me: bool

