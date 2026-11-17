from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional, Literal
from app.core.db import get_db
from app.api.deps import get_current_user, require_admin
from app.models import User, SnackCategory
from app.schemas.snack import (
    SnackCreate,
    SnackUpdate,
    SnackResponse,
    SnackListResponse,
    SummaryResponse,
    SnackQueryParams,
    ConsumeRequest,
    RestockRequest,
    VoteResponse
)
from app.services.snacks import (
    get_snacks,
    get_snack_by_id,
    create_snack,
    update_snack,
    delete_snack,
    get_summary,
    consume_snack,
    restock_snack,
    vote_snack,
    unvote_snack
)

router = APIRouter(prefix="/snacks", tags=["snacks"])


@router.get("/summary", response_model=SummaryResponse)
def get_snack_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_summary(db)


@router.get("", response_model=SnackListResponse)
def list_snacks(
    category: Optional[SnackCategory] = None,
    status: Optional[str] = None,
    q: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    sort_by: Literal["name", "quantity", "votes", "created_at"] = "name",
    order: Literal["asc", "desc"] = "asc",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_snacks(
        db=db,
        user_id=current_user.id,
        category=category,
        status=status,
        q=q,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order
    )


@router.get("/{snack_id}", response_model=SnackResponse)
def get_snack(
    snack_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_snack_by_id(db, snack_id, current_user.id)


@router.post("", response_model=SnackResponse, status_code=status.HTTP_201_CREATED)
def create_new_snack(
    snack_data: SnackCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return create_snack(
        db=db,
        user_id=current_user.id,
        name=snack_data.name,
        category=snack_data.category,
        quantity=snack_data.quantity,
        low_stock_threshold=snack_data.low_stock_threshold
    )


@router.patch("/{snack_id}", response_model=SnackResponse)
def update_existing_snack(
    snack_id: str,
    snack_data: SnackUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return update_snack(
        db=db,
        snack_id=snack_id,
        name=snack_data.name,
        category=snack_data.category,
        low_stock_threshold=snack_data.low_stock_threshold
    )


@router.delete("/{snack_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_snack(
    snack_id: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    delete_snack(db, snack_id)


@router.post("/{snack_id}/consume", response_model=SnackResponse)
def consume_existing_snack(
    snack_id: str,
    consume_data: ConsumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return consume_snack(db, snack_id, current_user.id, consume_data.amount)


@router.post("/{snack_id}/restock", response_model=SnackResponse)
def restock_existing_snack(
    snack_id: str,
    restock_data: RestockRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return restock_snack(db, snack_id, current_user.id, restock_data.amount)


@router.post("/{snack_id}/vote", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
def vote_for_snack(
    snack_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return vote_snack(db, snack_id, current_user.id)


@router.delete("/{snack_id}/vote", response_model=VoteResponse)
def unvote_for_snack(
    snack_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return unvote_snack(db, snack_id, current_user.id)

