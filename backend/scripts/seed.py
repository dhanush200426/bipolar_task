"""
Seed script for Snack Overflow.
Creates demo users and sample snacks with votes.
Idempotent - safe to run multiple times.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.core.security import hash_password
from app.models import User, UserRole, Snack, SnackCategory, Vote, Activity, ActivityAction
import uuid


def seed_users(db: Session):
    """Create demo admin and member users if they don't exist."""
    admin_password = os.getenv("SEED_ADMIN_PASSWORD", "admin123")
    member_password = os.getenv("SEED_MEMBER_PASSWORD", "member123")
    
    # Admin user
    admin = db.query(User).filter(User.email == "admin@snackoverflow.test").first()
    if not admin:
        admin = User(
            id=str(uuid.uuid4()),
            name="Demo Admin",
            email="admin@snackoverflow.test",
            password_hash=hash_password(admin_password),
            role=UserRole.ADMIN
        )
        db.add(admin)
        print("Created admin user: admin@snackoverflow.test")
    else:
        print("Admin user already exists: admin@snackoverflow.test")
    
    # Member user
    member = db.query(User).filter(User.email == "member@snackoverflow.test").first()
    if not member:
        member = User(
            id=str(uuid.uuid4()),
            name="Demo Member",
            email="member@snackoverflow.test",
            password_hash=hash_password(member_password),
            role=UserRole.MEMBER
        )
        db.add(member)
        print("Created member user: member@snackoverflow.test")
    else:
        print("Member user already exists: member@snackoverflow.test")
    
    db.commit()
    return admin, member


def seed_snacks(db: Session, admin_user: User, member_user: User):
    """Create sample snacks across all categories."""
    snack_data = [
        # Sweet category
        {"name": "Chocolate Bar", "category": SnackCategory.SWEET, "quantity": 10, "low_stock_threshold": 5},
        {"name": "Cookies", "category": SnackCategory.SWEET, "quantity": 0, "low_stock_threshold": 5},  # gone
        {"name": "Gummy Bears", "category": SnackCategory.SWEET, "quantity": 3, "low_stock_threshold": 5},  # running_low
        {"name": "Candy Canes", "category": SnackCategory.SWEET, "quantity": 20, "low_stock_threshold": 5},
        
        # Savoury category
        {"name": "Masala Peanuts", "category": SnackCategory.SAVOURY, "quantity": 15, "low_stock_threshold": 5},
        {"name": "Potato Chips", "category": SnackCategory.SAVOURY, "quantity": 8, "low_stock_threshold": 5},
        {"name": "Pretzels", "category": SnackCategory.SAVOURY, "quantity": 2, "low_stock_threshold": 5},  # running_low
        {"name": "Cheese Crackers", "category": SnackCategory.SAVOURY, "quantity": 25, "low_stock_threshold": 5},
        
        # Drink category
        {"name": "Cola", "category": SnackCategory.DRINK, "quantity": 12, "low_stock_threshold": 5},
        {"name": "Orange Juice", "category": SnackCategory.DRINK, "quantity": 4, "low_stock_threshold": 5},  # running_low
        {"name": "Green Tea", "category": SnackCategory.DRINK, "quantity": 18, "low_stock_threshold": 5},
        
        # Healthy-ish category
        {"name": "Apple", "category": SnackCategory.HEALTHYISH, "quantity": 6, "low_stock_threshold": 5},
        {"name": "Banana", "category": SnackCategory.HEALTHYISH, "quantity": 0, "low_stock_threshold": 5},  # gone
        {"name": "Mixed Nuts", "category": SnackCategory.HEALTHYISH, "quantity": 14, "low_stock_threshold": 5},
    ]
    
    snacks = {}
    for data in snack_data:
        snack = db.query(Snack).filter(Snack.name == data["name"]).first()
        if not snack:
            snack = Snack(
                id=str(uuid.uuid4()),
                name=data["name"],
                category=data["category"],
                quantity=data["quantity"],
                low_stock_threshold=data["low_stock_threshold"]
            )
            db.add(snack)
            print(f"Created snack: {data['name']} ({data['category']})")
        else:
            print(f"Snack already exists: {data['name']}")
        snacks[data["name"]] = snack
    
    db.commit()
    return snacks


def seed_votes(db: Session, admin_user: User, member_user: User, snacks: dict):
    """Add some votes to snacks."""
    vote_data = [
        ("Chocolate Bar", admin_user),
        ("Chocolate Bar", member_user),
        ("Masala Peanuts", admin_user),
        ("Masala Peanuts", member_user),
        ("Masala Peanuts", admin_user),  # This should be ignored due to unique constraint
        ("Cola", admin_user),
        ("Cola", member_user),
        ("Mixed Nuts", admin_user),
        ("Mixed Nuts", member_user),
        ("Mixed Nuts", admin_user),  # This should be ignored
    ]
    
    for snack_name, user in vote_data:
        snack = snacks[snack_name]
        existing = db.query(Vote).filter(
            Vote.user_id == user.id,
            Vote.snack_id == snack.id
        ).first()
        if not existing:
            vote = Vote(user_id=user.id, snack_id=snack.id)
            db.add(vote)
            print(f"Added vote: {user.email} -> {snack_name}")
        else:
            print(f"Vote already exists: {user.email} -> {snack_name}")
    
    db.commit()


def main():
    """Run seed script."""
    print("=== Seeding Snack Overflow Database ===\n")
    
    db = SessionLocal()
    try:
        admin, member = seed_users(db)
        snacks = seed_snacks(db, admin, member)
        seed_votes(db, admin, member, snacks)
        
        print("\n=== Seed Complete ===")
        print("Demo credentials:")
        print("  Admin: admin@snackoverflow.test / admin123")
        print("  Member: member@snackoverflow.test / member123")
        
    except Exception as e:
        print(f"Error during seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
