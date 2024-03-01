from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from icecream import ic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.configurations.database import get_async_session
from src.schemas import ReturnedBook
from src.schemas.sellers import ReturnedSeller, IncomingSeller, ReturnedAllSellers, BaseSeller
from src.models.sellers import Seller

sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@sellers_router.post("/", response_model=ReturnedSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(
        seller: IncomingSeller, session: DBSession
):

    new_seller = Seller(
        first_name=seller.first_name,
        last_name=seller.last_name,
        email=seller.email,
        password=seller.password
    )

    session.add(new_seller)

    await session.flush()

    await session.refresh(new_seller, attribute_names=["books"])

    return new_seller


@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers(session: DBSession):
    query = select(Seller).options(selectinload(Seller.books))
    res = await session.execute(query)
    sellers = res.scalars().all()
    return {"sellers": sellers}


@sellers_router.get("/{seller_id}", response_model=ReturnedSeller)
async def get_seller(seller_id: int, session: DBSession):
    res = await session.get(Seller, seller_id)
    await session.refresh(res, attribute_names=["books"])
    return res


@sellers_router.delete("/{seller_id}")
async def delete_seller(seller_id: int, session: DBSession):
    deleted_seller = await session.get(Seller, seller_id)
    ic(deleted_seller)
    if deleted_seller:
        await session.delete(deleted_seller)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@sellers_router.put("/{seller_id}", response_model=BaseSeller)
async def update_seller(seller_id: int, new_data: BaseSeller, session: DBSession):
    if updated_seller := await session.get(Seller, seller_id):
        updated_seller.email = new_data.email
        updated_seller.first_name = new_data.first_name
        updated_seller.last_name = new_data.last_name

        await session.flush()

        return updated_seller

    return Response(status_code=status.HTTP_404_NOT_FOUND)
