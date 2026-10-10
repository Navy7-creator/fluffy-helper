
from sqlalchemy import   create_engine, false, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app 
from fastapi.testclient import TestClient
import pytest
from ..models import Todos,Users
from ..routers.auth import bcrypt_context





from sqlalchemy.orm import declarative_base
Base = declarative_base()


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} ,
    poolclass=StaticPool ,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()  

def override_get_current_user():
    return {"username": "lemon", "id": 1, "user_role": "admin"}


@pytest.fixture
def test_todo():
    todo = Todos(title="Test Todo",
                  description="This is a test todo", 
                  priority=1, 
                  complete=False,
                  owner_id=1
                  )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()


@pytest.fixture
def test_user():
    password = "on"[:72]
    hashed_password = bcrypt_context.hash(password)
    user = Users(
        username="lemon",  
        email="lemonie@gmail.com",
        first_name="string",
        last_name="lem",
        hashed_password=hashed_password,
        role="admin",
        phone_number=""
    )
    db = TestingSessionLocal()
    db.add(user)    
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()

    