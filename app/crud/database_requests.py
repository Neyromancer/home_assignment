from fastapi import HTTPException
from sqlalchemy import select
# TODO: check type of error and their use
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database_data_models import ApplicationDBModel
from app.schemas.database_validation_schemas import ApplicationBase, ApplicationResponse, ApplicationCreate

async def fetch_by_username(database_session: AsyncSession, username: str) -> list[ApplicationDBModel]:
    try:
        database_query = select(ApplicationDBModel).where(ApplicationDBModel.username == username)
        database_query_result = (await database_session.scalars(database_query))
        database_fetched_applications = database_query_result.fetchall()
        if not database_fetched_applications:
            raise HTTPException(status_code=404, detail=f"Applications created by {username} not found")

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    return database_fetched_applications

# in case of large dataset cursor could be used: 
# https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results
async def fetch_all(database_session: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        database_query = select(ApplicationDBModel).offset(skip).limit(limit)
        database_query_result = (await database_session.scalars(database_query))
        database_fetched_applications = database_query_result.fetchall()
        if not database_fetched_applications:
            raise HTTPException(status_code=404, detail="Failed to fetch applications from Database")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
    return database_fetched_applications

async def create(database_session: AsyncSession, application_to_save: ApplicationCreate) -> ApplicationDBModel:
    application = ApplicationDBModel(**application_to_save.model_dump(exclude_unset=True))
    database_session.add(application)
    try:
        await database_session.commit()
        # TODO: Learn what is this for?
        await database_session.refresh(application)
    except SQLAlchemyError as e:
        await database_session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to store application in database. Error: {str(e)}")
    return application