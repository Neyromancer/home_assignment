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
    # return ApplicationResponse.model_validate(fake_application_db[application_id])
    application = await application.fetch_by_id(application_id, db_session)
    return list(map(ApplicationResponse.from_orm, application))


@router.get("/", response_model=list[ApplicationResponse])
def get_applications(db_session: AsyncSession) -> list[ApplicationResponse]:
    # return [ApplicationResponse.model_validate(val) for index, val in fake_application_db.items()]
    applications = await application.fetch_all(db_session)
    return [ApplicationResponse.model_validate(application) for application in applications]


@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db_session: AsyncSession) -> ApplicationResponse:
    application = await application.create(application, db_session)
    return ApplicationResponse.from_orm(application)
    # if db_id[0] < 6:
    #     db_id[0] += 1
    # else:
    #     db_id[0] = 1
    # fake_application_db[db_id[0]] = {"id": db_id[0], "username": f"TestUser{db_id[0]}", "description": f"TestUser{db_id[0]} application description", "created_at": f"2025-01-21T14:{db_id[0]}0:{db_id[0]}5.337Z"}
    # return ApplicationResponse.model_validate(fake_application_db[db_id[0]]) 
