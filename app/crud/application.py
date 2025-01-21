from fastapi import HTTPException
from sqlalchemy import select
# TODO: check type of error and their use
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import ApplicationDBModel
from app.schemas.application import ApplicationBase, ApplicationResponse, ApplicationCreate

async def fetch_by_username(db_session: AsyncSession, username: str) -> list[ApplicationDBModel]:
    try:
        query = select(ApplicationDBModel).where(ApplicationDBModel.username == username)
        query_result = (await db_session.scalars(query))
        fetched_applications = query_result.fetchall()
        if not fetched_applications:
            raise HTTPException(status_code=404, detail=f"Applications created by {username} not found")

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    return fetched_applications

# in case of large dataset cursor could be used: 
# https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results
async def fetch_all(db_session: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        query = select(ApplicationDBModel).offset(skip).limit(limit)
        query_result = (await db_session.scalars(query))
        fetched_applications = query_result.fetchall()
        if not fetched_applications:
            raise HTTPException(status_code=404, detail="Failed to fetch applications from Database")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    return fetched_applications

async def create(db_session: AsyncSession, application: ApplicationCreate) -> ApplicationDBModel:
    application = ApplicationDBModel(**application_data.model_dump(exclude_unset=True))
    db_session.add(application)
    try:
        await db_session.commit()
        # TODO: Learn what is this for?
        await db_session.refresh(application)
    except SQLAlchemyError as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to store application in database. Error: {str(e)}")
    return application