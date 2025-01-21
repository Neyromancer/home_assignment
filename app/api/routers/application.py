from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import application
from schemas.application import ApplicationBase, ApplicationResponse, ApplicationCreate
from models.application import ApplicationDBModel
from database import get_db_session


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    dependencies=[Depends(get_db_session)],
    responses={404: {"description": "Not Found"}}
)

# Use it to test API work
fake_application_db = {1: {"id": 1, "username": "TestUser1", "description": "TestUser1 application description", "created_at": "2025-01-21T14:00:05.337Z"}, 2: {"id": 2, "username": "TestUser2", "description": "TestUser2 application description", "created_at": "2025-01-21T14:05:05.337Z"}}
db_id: list[int] = [2]

# TODO: add caching for fast retrieval
@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
async def application_details(application_id: int, db_session: AsyncSession) -> ApplicationResponse:
    application = await application.fetch_by_id(application_id, db_session)
    return list(map(ApplicationResponse.from_orm, application))


@router.get("/", response_model=list[ApplicationResponse])
def get_applications(db_session: AsyncSession) -> list[ApplicationResponse]:
    applications = await application.fetch_all(db_session)
    return [ApplicationResponse.model_validate(application) for application in applications]


@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db_session: AsyncSession) -> ApplicationResponse:
    application = await application.create(application, db_session)
    return ApplicationResponse.from_orm(application)
