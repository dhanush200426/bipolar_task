from sqlalchemy.orm import Session
from sqlalchemy import func, case, literal_column, select, and_, or_
from sqlalchemy.exc import IntegrityError
from typing import Optional, Literal
from app.models import Snack, Vote, Activity, ActivityAction, SnackCategory
from app.core.errors import AppError, ErrorCode
from app.services.snack_status import get_snack_status_case_expression, get_snack_status


def get_snacks(
    db: Session,
    user_id: str,
    category: Optional[SnackCategory] = None,
    status: Optional[str] = None,
    q: Optional[str] = None,
    page: int = 1,
    page_size: int = 12,
    sort_by: Literal["name", "quantity", "votes", "created_at"] = "name",
    order: Literal["asc", "desc"] = "asc"
):
    status_expr = get_snack_status_case_expression(Snack.quantity, Snack.low_stock_threshold)
    
    vote_count_subq = (
        select(func.count(Vote.id))
        .where(Vote.snack_id == Snack.id)
        .correlate(Snack)
        .scalar_subquery()
    )
    
    voted_by_me_subq = (
        select(func.count(Vote.id))
        .where(and_(Vote.snack_id == Snack.id, Vote.user_id == user_id))
        .correlate(Snack)
        .scalar_subquery()
    )
    
    query = (
        select(
            Snack,
            status_expr.label("status"),
            vote_count_subq.label("vote_count"),
            voted_by_me_subq.label("voted_by_me")
        )
    )
    
    if category:
        query = query.where(Snack.category == category)
    
    if status:
        query = query.where(status_expr == literal_column(f"'{status}'"))
    
    if q:
        escaped_q = q.replace("%", "\\%").replace("_", "\\_")
        query = query.where(Snack.name.ilike(f"%{escaped_q}%"))
    
    sort_column = {
        "name": Snack.name,
        "quantity": Snack.quantity,
        "votes": vote_count_subq,
        "created_at": Snack.created_at
    }[sort_by]
    
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    results = db.execute(query).all()
    
    pages = (total + page_size - 1) // page_size if total > 0 else 0
    
    items = []
    for row in results:
        snack = row[0]
        items.append({
            "id": snack.id,
            "name": snack.name,
            "category": snack.category,
            "quantity": snack.quantity,
            "low_stock_threshold": snack.low_stock_threshold,
            "status": row.status,
            "vote_count": row.vote_count or 0,
            "voted_by_me": row.voted_by_me > 0,
            "created_at": snack.created_at.isoformat(),
            "updated_at": snack.updated_at.isoformat()
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages
    }


def get_snack_by_id(db: Session, snack_id: str, user_id: str):
    status_expr = get_snack_status_case_expression(Snack.quantity, Snack.low_stock_threshold)
    
    vote_count_subq = (
        select(func.count(Vote.id))
        .where(Vote.snack_id == Snack.id)
        .scalar_subquery()
    )
    
    voted_by_me_subq = (
        select(func.count(Vote.id))
        .where(and_(Vote.snack_id == Snack.id, Vote.user_id == user_id))
        .scalar_subquery()
    )
    
    query = (
        select(
            Snack,
            status_expr.label("status"),
            vote_count_subq.label("vote_count"),
            voted_by_me_subq.label("voted_by_me")
        )
        .where(Snack.id == snack_id)
    )
    
    result = db.execute(query).first()
    
    if not result:
        raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
    
    snack = result[0]
    return {
        "id": snack.id,
        "name": snack.name,
        "category": snack.category,
        "quantity": snack.quantity,
        "low_stock_threshold": snack.low_stock_threshold,
        "status": result.status,
        "vote_count": result.vote_count or 0,
        "voted_by_me": result.voted_by_me > 0,
        "created_at": snack.created_at.isoformat(),
        "updated_at": snack.updated_at.isoformat()
    }


def create_snack(db: Session, user_id: str, name: str, category: SnackCategory, quantity: int, low_stock_threshold: int):
    try:
        snack = Snack(
            name=name,
            category=category,
            quantity=quantity,
            low_stock_threshold=low_stock_threshold
        )
        db.add(snack)
        
        if quantity > 0:
            activity = Activity(
                user_id=user_id,
                snack_id=snack.id,
                snack_name=name,
                action=ActivityAction.RESTOCKED,
                amount=quantity
            )
            db.add(activity)
        
        db.commit()
        db.refresh(snack)
        
        status = get_snack_status(snack.quantity, snack.low_stock_threshold)
        
        return {
            "id": snack.id,
            "name": snack.name,
            "category": snack.category,
            "quantity": snack.quantity,
            "low_stock_threshold": snack.low_stock_threshold,
            "status": status,
            "vote_count": 0,
            "voted_by_me": False,
            "created_at": snack.created_at.isoformat(),
            "updated_at": snack.updated_at.isoformat()
        }
    except IntegrityError:
        db.rollback()
        raise AppError(status_code=409, code=ErrorCode.SNACK_NAME_TAKEN, message="Snack name already exists")


def update_snack(db: Session, snack_id: str, name: Optional[str], category: Optional[SnackCategory], low_stock_threshold: Optional[int]):
    snack = db.query(Snack).filter(Snack.id == snack_id).first()
    
    if not snack:
        raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
    
    if name is not None:
        snack.name = name
    if category is not None:
        snack.category = category
    if low_stock_threshold is not None:
        snack.low_stock_threshold = low_stock_threshold
    
    try:
        db.commit()
        db.refresh(snack)
        
        status = get_snack_status(snack.quantity, snack.low_stock_threshold)
        
        return {
            "id": snack.id,
            "name": snack.name,
            "category": snack.category,
            "quantity": snack.quantity,
            "low_stock_threshold": snack.low_stock_threshold,
            "status": status,
            "vote_count": 0,
            "voted_by_me": False,
            "created_at": snack.created_at.isoformat(),
            "updated_at": snack.updated_at.isoformat()
        }
    except IntegrityError:
        db.rollback()
        raise AppError(status_code=409, code=ErrorCode.SNACK_NAME_TAKEN, message="Snack name already exists")


def delete_snack(db: Session, snack_id: str):
    snack = db.query(Snack).filter(Snack.id == snack_id).first()
    
    if not snack:
        raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
    
    db.delete(snack)
    db.commit()


def get_summary(db: Session):
    status_expr = get_snack_status_case_expression(Snack.quantity, Snack.low_stock_threshold)
    
    vote_count_subq = (
        select(func.count(Vote.id))
        .where(Vote.snack_id == Snack.id)
        .scalar_subquery()
    )
    
    # Get status counts
    status_counts = (
        select(
            status_expr.label("status"),
            func.count().label("count")
        )
        .group_by(status_expr)
    )
    
    status_result = db.execute(status_counts).all()
    
    counts = {"stocked": 0, "running_low": 0, "gone": 0}
    for row in status_result:
        if row.status in counts:
            counts[row.status] = row.count
    
    total = db.scalar(select(func.count()).select_from(Snack))
    
    # Get snack of the week
    snack_of_week_query = (
        select(
            Snack,
            status_expr.label("status"),
            vote_count_subq.label("vote_count")
        )
        .where(vote_count_subq > 0)
        .order_by(vote_count_subq.desc(), Snack.name.asc())
        .limit(1)
    )
    
    snack_of_week_result = db.execute(snack_of_week_query).first()
    
    snack_of_week = None
    if snack_of_week_result:
        snack = snack_of_week_result[0]
        snack_of_week = {
            "id": snack.id,
            "name": snack.name,
            "category": snack.category,
            "vote_count": snack_of_week_result.vote_count,
            "quantity": snack.quantity,
            "status": snack_of_week_result.status
        }
    
    return {
        "stocked": counts["stocked"],
        "running_low": counts["running_low"],
        "gone": counts["gone"],
        "total": total,
        "snack_of_the_week": snack_of_week
    }


def consume_snack(db: Session, snack_id: str, user_id: str, amount: int):
    """
    Atomically consume a snack quantity.
    
    This uses a single UPDATE statement with RETURNING to:
    1. Check if the snack exists and has sufficient stock
    2. Decrease the quantity atomically
    3. Return the updated row if successful
    
    The UPDATE takes a row-level lock. Under READ COMMITTED isolation (PostgreSQL default),
    concurrent UPDATEs re-evaluate the WHERE clause after acquiring the lock. This ensures
    that if two transactions try to consume the same item, only those that pass the WHERE
    clause (quantity >= amount) will succeed. The CHECK constraint (quantity >= 0) is the
    final safety net if something bypasses the WHERE clause.
    """
    from sqlalchemy import update, literal_column
    from datetime import datetime
    
    try:
        # Atomic UPDATE with RETURNING
        update_stmt = (
            update(Snack)
            .where(Snack.id == snack_id)
            .where(Snack.quantity >= amount)
            .values(
                quantity=Snack.quantity - amount,
                updated_at=datetime.utcnow()
            )
            .returning(
                Snack.id,
                Snack.name,
                Snack.category,
                Snack.quantity,
                Snack.low_stock_threshold
            )
        )
        
        result = db.execute(update_stmt).first()
        
        if not result:
            # UPDATE returned no row - either snack doesn't exist or insufficient stock
            # Do a lookup to distinguish the two cases
            snack = db.query(Snack).filter(Snack.id == snack_id).first()
            
            if not snack:
                raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
            
            if snack.quantity == 0:
                raise AppError(status_code=409, code=ErrorCode.INSUFFICIENT_STOCK, message="This snack is gone")
            else:
                raise AppError(
                    status_code=409,
                    code=ErrorCode.INSUFFICIENT_STOCK,
                    message=f"Someone beat you to it. Only {snack.quantity} left."
                )
        
        snack_id, name, category, quantity, low_stock_threshold = result
        
        # Insert activity row in the same transaction
        activity = Activity(
            user_id=user_id,
            snack_id=snack_id,
            snack_name=name,
            action=ActivityAction.CONSUMED,
            amount=amount
        )
        db.add(activity)
        
        db.commit()
        
        status = get_snack_status(quantity, low_stock_threshold)
        
        return {
            "id": snack_id,
            "name": name,
            "category": category,
            "quantity": quantity,
            "low_stock_threshold": low_stock_threshold,
            "status": status,
            "vote_count": 0,
            "voted_by_me": False,
            "created_at": "",  # Not needed for consume response
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception:
        db.rollback()
        raise


def restock_snack(db: Session, snack_id: str, user_id: str, amount: int):
    """
    Atomically restock a snack quantity.
    """
    from sqlalchemy import update
    from datetime import datetime
    
    try:
        # Atomic UPDATE with RETURNING
        update_stmt = (
            update(Snack)
            .where(Snack.id == snack_id)
            .values(
                quantity=Snack.quantity + amount,
                updated_at=datetime.utcnow()
            )
            .returning(
                Snack.id,
                Snack.name,
                Snack.category,
                Snack.quantity,
                Snack.low_stock_threshold
            )
        )
        
        result = db.execute(update_stmt).first()
        
        if not result:
            raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
        
        snack_id, name, category, quantity, low_stock_threshold = result
        
        # Insert activity row in the same transaction
        activity = Activity(
            user_id=user_id,
            snack_id=snack_id,
            snack_name=name,
            action=ActivityAction.RESTOCKED,
            amount=amount
        )
        db.add(activity)
        
        db.commit()
        
        status = get_snack_status(quantity, low_stock_threshold)
        
        return {
            "id": snack_id,
            "name": name,
            "category": category,
            "quantity": quantity,
            "low_stock_threshold": low_stock_threshold,
            "status": status,
            "vote_count": 0,
            "voted_by_me": False,
            "created_at": "",
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except Exception:
        db.rollback()
        raise


def vote_snack(db: Session, snack_id: str, user_id: str):
    """
    Vote for a snack. Relies on UNIQUE constraint to prevent duplicate votes.
    """
    from sqlalchemy import select, func
    
    try:
        # Check if snack exists first
        snack = db.query(Snack).filter(Snack.id == snack_id).first()
        if not snack:
            raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
        
        # Try to insert vote - UNIQUE constraint will fail if already voted
        vote = Vote(user_id=user_id, snack_id=snack_id)
        db.add(vote)
        db.commit()
        
        # Get updated vote count
        vote_count = db.scalar(select(func.count(Vote.id)).where(Vote.snack_id == snack_id))
        
        return {
            "vote_count": vote_count,
            "voted_by_me": True
        }
        
    except IntegrityError:
        db.rollback()
        # Check if it's a duplicate vote or missing snack
        existing_vote = db.query(Vote).filter(
            and_(Vote.user_id == user_id, Vote.snack_id == snack_id)
        ).first()
        if existing_vote:
            raise AppError(status_code=409, code=ErrorCode.ALREADY_VOTED, message="Already voted for this snack")
        else:
            raise AppError(status_code=404, code=ErrorCode.SNACK_NOT_FOUND, message="Snack not found")
    except Exception:
        db.rollback()
        raise


def unvote_snack(db: Session, snack_id: str, user_id: str):
    """
    Remove vote for a snack. Idempotent-safe under concurrency.
    """
    from sqlalchemy import delete
    
    try:
        # DELETE with RETURNING to check if vote existed
        delete_stmt = (
            delete(Vote)
            .where(and_(Vote.user_id == user_id, Vote.snack_id == snack_id))
            .returning(Vote.id)
        )
        
        result = db.execute(delete_stmt).first()
        
        if not result:
            raise AppError(status_code=404, code=ErrorCode.VOTE_NOT_FOUND, message="Vote not found")
        
        db.commit()
        
        # Get updated vote count
        from sqlalchemy import select, func
        vote_count = db.scalar(select(func.count(Vote.id)).where(Vote.snack_id == snack_id))
        
        return {
            "vote_count": vote_count,
            "voted_by_me": False
        }
        
    except Exception:
        db.rollback()
        raise

