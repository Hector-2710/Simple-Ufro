import pytest
from httpx import AsyncClient
from app.core import security
from app.models.user import User, Role
import uuid

@pytest.mark.asyncio
async def test_login_access_token(client: AsyncClient, db_session):
    email = "test@example.com"
    username = "testuser"
    password = "testpassword"
    hashed_password = security.get_password_hash(password)
    
    test_user = User(
        id=uuid.uuid4(),
        email=email,
        username=username,
        full_name="Test User",
        hashed_password=hashed_password,
        role=Role.STUDENT,
        is_active=True
    )
    db_session.add(test_user)
    await db_session.commit()
    
    login_data = {
        "username": username,
        "password": password
    }
    response = await client.post("/api/v1/login/access-token", data=login_data)
    
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/login/access-token", data=login_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"

