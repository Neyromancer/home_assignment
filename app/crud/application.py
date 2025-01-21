from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.application import ApplicationDBModel
from schemas.application import ApplicationResponse, ApplicationBase

async def fetch_by_id(application_id: int, db_session = None) -> ApplicationDBModel:
    application = (await db_session.scalars(select(ApplicationDBModel).where(ApplicationDBModel.id == application_id))).first()
    if not application:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    return application

# in case of large dataset cursor could be used: 
# https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results
async def fetch(db_session = None):
    applications = (await db_session.scalars(select(ApplicationDBModel))).fetchall()
    if not applications:
        raise HTTPException(status_code=404, detail=f"Failed to fetch applications from Database")
    return applications

async def create(application: ApplicationBase, db_session = None) -> ApplicationDBModel:
    application = ApplicationDBModel(**application.dict())
    db_session.add(application)
    await db_session.commit()
    return application