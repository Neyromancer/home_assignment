from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import database_requests
from app.schemas.database_validation_schemas import (
    ApplicationBase,
    ApplicationResponse,
    ApplicationCreate,
)
from app.models.database_data_models import ApplicationDBModel
from app.database import get_database_session


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    responses={404: {"description": "Not Found"}},
)


@router.get(
    "/",
    response_model=list[ApplicationResponse],
    summary="Get all applications",
    description="Retrieve all applications with optional pagination",
)
async def get_all_applications(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    database_session: AsyncSession = Depends(get_database_session),
) -> list[ApplicationResponse]:
    fetched_applications = await database_requests.fetch_all(
        database_session, skip=(page - 1) * size, limit=size
    )
    return [
        ApplicationResponse.model_validate(application)
        for application in fetched_applications
    ]


# TODO: Check what is the best practice for filtering
@router.get(
    "/{username}",
    response_model=list[ApplicationResponse],
    summary="Get applications by username",
)
async def get_applications_by_user(
    username: str, database_session: AsyncSession = Depends(get_database_session)
) -> list[ApplicationResponse]:
    fetched_user_applications = await database_requests.fetch_by_username(
        database_session, username
    )
    return list(map(ApplicationResponse.from_orm, fetched_user_applications))


@router.post(
    "/",
    response_model=ApplicationResponse,
    status_code=201,
    summary="Create a new application",
)
async def create_application(
    application_to_save: ApplicationCreate,
    database_session: AsyncSession = Depends(get_database_session),
) -> ApplicationResponse:
    database_saved_application = await database_requests.create(
        database_session, application_to_save
    )
    return ApplicationResponse.from_orm(database_saved_application)
