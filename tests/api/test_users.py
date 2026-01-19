import pytest
from httpx import AsyncClient
from app.models.user import Role
import uuid
from app.core import security
from app.models.user import User

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword",
        "full_name": "New User"
    }
    response = await client.post("/api/v1/users/", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data

@pytest.mark.asyncio
async def test_read_user_me(client: AsyncClient, db_session):
    test_user = User(
        id=uuid.uuid4(),
        email="me@example.com",
        username="meuser",
        full_name="Me User",
        hashed_password=security.get_password_hash("me_password"),
        role=Role.STUDENT,
        is_active=True
    )
    db_session.add(test_user)
    await db_session.commit()
    
    login_response = await client.post("/api/v1/login/access-token", data={"username": "meuser", "password": "me_password"})
    token = login_response.json()["access_token"]
    
    response = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"
    assert data["email"] == "me@example.com"

@pytest.mark.asyncio
async def test_update_user_me(client: AsyncClient, db_session):
    test_user = User(
        id=uuid.uuid4(),
        email="update@example.com",
        username="updateuser",
        full_name="Update User",
        hashed_password=security.get_password_hash("update_password"),
        role=Role.STUDENT,
        is_active=True
    )
    db_session.add(test_user)
    await db_session.commit()
    
    login_response = await client.post("/api/v1/login/access-token", data={"username": "updateuser", "password": "update_password"})
    token = login_response.json()["access_token"]
    
    update_data = {"full_name": "Updated Name"}
    response = await client.patch("/api/v1/users/me", json=update_data, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    
   