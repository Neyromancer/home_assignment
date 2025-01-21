from fastapi import HTTPException
from sqlalchemy import select
# TODO: check type of error and their use
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.application import ApplicationDBModel
from schemas.application import ApplicationBase, ApplicationResponse, ApplicationCreate

async def fetch_by_id(application_id: int, db_session: AsyncSession) -> ApplicationDBModel:
    try:
        application = (await db_session.scalars(select(ApplicationDBModel).where(ApplicationDBModel.id == application_id))).first()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")
    return application

# in case of large dataset cursor could be used: 
# https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results
async def fetch_all(db_session: AsyncSession):
    applications = (await db_session.scalars(select(ApplicationDBModel))).fetchall()
    if not applications:
        raise HTTPException(status_code=404, detail=f"Failed to fetch applications from Database")
    return applications

async def create(application: ApplicationCreate, db_session: AsyncSession) -> ApplicationDBModel:
    application = ApplicationDBModel(**application.dict())
    db_session.add(application)
    await db_session.commit()
    # TODO: Learn what is this for?
    await db_session.refresh(application)
    return application