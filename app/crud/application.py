from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import application as ApplicationDBModel

async def get_application_by_id(application_id: int, db_session: AsyncSession = None) -> ApplicationDBModel:

    return 

async def place_application(db_session: AsyncSession = None) -> None:
    print("Writing to DB: ")