from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import application as ApplicationDBModel

async def get_application_by_id(application_id: int, db_session: AsyncSession = None):
    application = (await db_session.scalars(select(ApplicationDBModel).where(ApplicationDBModel.id == application_id))).first()
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    return application

async def place_application(db_session: AsyncSession = None) -> None:
    print("Writing to DB: ")