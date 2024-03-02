import pytest
from fastapi import status

from src.models import sellers


@pytest.mark.asyncio
async def test_get_seller(async_client, db_session):
    seller = sellers.Seller(first_name="John", last_name="Doe", email="johndoe@example.com", password="password")
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_200_OK
    result_data = response.json()

    assert result_data["id"] == seller.id
    assert result_data["first_name"] == seller.first_name
    assert result_data["last_name"] == seller.last_name
    assert result_data["email"] == seller.email
    assert "password" not in result_data  


@pytest.mark.asyncio
async def test_update_seller(async_client, db_session):
    seller = sellers.Seller(first_name="John", last_name="Doe", email="johndoe@example.com", password="password")
    db_session.add(seller)
    await db_session.flush()

    update_data = {
        "first_name": "Updated Name",
        "last_name": "Updated Last Name",
        "email": "updatedemail@example.com"
    }
    response = await async_client.put(f"/api/v1/sellers/{seller.id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    result_data = response.json()

    assert result_data["first_name"] == update_data["first_name"]
    assert result_data["last_name"] == update_data["last_name"]
    assert result_data["email"] == update_data["email"]


@pytest.mark.asyncio
async def test_create_seller(async_client, db_session):
    data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alicesmith@example.com",
        "password": "password123"
    }
    response = await async_client.post("/api/v1/sellers/", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    result_data = response.json()

    assert "id" in result_data
    assert result_data["first_name"] == data["first_name"]
    assert result_data["last_name"] == data["last_name"]
    assert result_data["email"] == data["email"]


@pytest.mark.asyncio
async def test_get_all_sellers(async_client, db_session):
    response = await async_client.get("/api/v1/sellers/")

    assert response.status_code == status.HTTP_200_OK
    result_data = response.json()

    assert "sellers" in result_data
    assert isinstance(result_data["sellers"], list)


@pytest.mark.asyncio
async def test_delete_seller(async_client, db_session):
    seller = sellers.Seller(first_name="Emily", last_name="Jones", email="emilyjones@example.com",
                            password="password456")
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
