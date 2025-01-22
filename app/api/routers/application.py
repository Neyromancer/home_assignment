from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import database_requests
from app.schemas.database_validation_schemas import ApplicationBase, ApplicationResponse, ApplicationCreate
from app.models.database_data_models import ApplicationDBModel
from app.database import get_database_session

# ##########################################################
# TODO: Add support for pagination (parameters: page и size).
# ##########################################################

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    # dependencies=[Depends(get_database_session)],
    responses={404: {"description": "Not Found"}}
)

# Use it to test API work
fake_application_db = {1: {"id": 1, "username": "TestUser1", "description": "TestUser1 application description", "creation_time": "2025-01-21T14:00:05.337Z"}, 2: {"id": 2, "username": "TestUser2", "description": "TestUser2 application description", "creation_time": "2025-01-21T14:05:05.337Z"}}
db_id: list[int] = [2]

# TODO: add caching for fast retrieval
# TODO: Check what is the best practice for filtering
@router.get("/{username}", response_model=list[ApplicationResponse])
async def application_details(username: str, database_session: AsyncSession = Depends(get_database_session)) -> list[ApplicationResponse]:
    fetched_user_applications = await database_requests.fetch_by_username(database_session, username)
    return list(map(ApplicationResponse.from_orm, fetched_user_applications))


@router.get("/", response_model=list[ApplicationResponse])
async def get_applications(page: int = Query(1, ge=1, description="Page number"), size: int = Query(10, ge=1, le=100, description="Items per page"), database_session: AsyncSession = Depends(get_database_session)) -> list[ApplicationResponse]:
    # Why is this strange formula ` skip=(page - 1) * size` used?
    fetched_applications = await database_requests.fetch_all(database_session, skip=(page - 1) * size, limit=size)
    return [ApplicationResponse.model_validate(application) for application in fetched_applications]


@router.post("/", response_model=ApplicationResponse)
async def create_application(application_to_save: ApplicationCreate, database_session: AsyncSession = Depends(get_database_session)) -> ApplicationResponse:
    database_saved_application = await database_requests.create(database_session, application_to_save)
    return ApplicationResponse.from_orm(database_saved_application)
