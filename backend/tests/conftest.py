"""
Pytest configuration and fixtures for Snack Overflow tests.
Uses a separate test database (snackoverflow_test) to avoid affecting dev data.
"""
import pytest
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from app.core.db import Base, get_db
from app.models import User, Snack, Vote, Activity
from app.core.config import settings
from fastapi.testclient import TestClient
from app.main import app


# Test database URL
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://snackoverflow:snackoverflow@localhost:5432/snackoverflow_test"
)

# Create test engine with StaticPool for in-memory-like behavior
test_engine = create_engine(
    TEST_DATABASE_URL,
    poolclass=StaticPool,
    echo=False
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test.
    Creates tables directly, runs test, then drops tables.
    """
    # Create all tables directly
    Base.metadata.create_all(bind=test_engine)
    
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client that uses the test database session.
    """
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing."""
    from app.core.security import hash_password
    from app.models.user import UserRole
    import uuid
    
    user = User(
        id=str(uuid.uuid4()),
        name="Test Admin",
        email="admin@test.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def member_user(db_session):
    """Create a member user for testing."""
    from app.core.security import hash_password
    from app.models.user import UserRole
    import uuid
    
    user = User(
        id=str(uuid.uuid4()),
        name="Test Member",
        email="member@test.com",
        password_hash=hash_password("member123"),
        role=UserRole.MEMBER
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_snack(db_session):
    """Create a sample snack for testing."""
    import uuid
    from app.models import SnackCategory
    
    snack = Snack(
        id=str(uuid.uuid4()),
        name="Test Snack",
        category=SnackCategory.SWEET,
        quantity=10,
        low_stock_threshold=5
    )
    db_session.add(snack)
    db_session.commit()
    db_session.refresh(snack)
    return snack
