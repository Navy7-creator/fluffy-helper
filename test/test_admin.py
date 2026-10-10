from .utils import *
from ..routers.admin import get_db as admin_get_db
from ..routers.auth import get_current_user
from fastapi import status
from ..models import Todos

app.dependency_overrides[admin_get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_read_all_authenticated(test_todo):
    response = client.get("/admin/todo/")
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    data = response.json()
    assert any(todo["id"] == test_todo.id for todo in data)


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model= db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_todo_not_found(): 
    
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}






