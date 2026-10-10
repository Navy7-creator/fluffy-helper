from .utils import *
from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)
from urllib import response
from sqlalchemy.orm import declarative_base
Base = declarative_base()

def test_read_all_authenticated(test_todo: Todos):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1,"title":"Test Todo",
                  "description":"This is a test todo", 
                  "priority":1, 
                  "complete":False,
                  "owner_id":1}]  # Assuming the database is empty for this test    

def test_read_one_authenticated(test_todo: Todos):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK   
    assert response.json() == { "id": 1,"title":"Test Todo",
                  "description":"This is a test todo", 
                  "priority":1, 
                  "complete":False,
                  "owner_id":1}  # Assuming the database is empty for this test



def test_read_one_authenticated_not_found(test_todo: Todos):
    response=client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}

def test_new_todo_authenticated():
    request_data = {"title": "New Todo", "description": "This is a new todo", "priority": 2, "complete": False}
    response = client.post("/todos/todo/", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    todo = db.query(Todos).filter(Todos.title == "New Todo").first()
    assert todo.title == request_data.get("title")
    assert todo.description == request_data.get("description")
    assert todo.priority == request_data.get("priority")
    assert todo.complete == request_data.get("complete")

def test_update_todo(test_todo: Todos):
    request_data = {"title": "Updated Todo", "description": "This is an updated todo", "priority": 3, "complete": False}
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Updated Todo"


def test_update_todo_not_found():
    request_data = {"title": "Updated Todo", "description": "This is an updated todo", "priority": 3, "complete": False}
    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}

def test_delete_todo(test_todo: Todos):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None    

def test_delete_todo_not_found(test_todo: Todos):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}
    
    