from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import application
from app.schemas.application import ApplicationResponse, ApplicationBase
from app.models.application import ApplicationDBModel


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    responses={404: {"description": "Not Found"}}
)

# TODO: add caching for fast retrieval
@router.get(
    "/{application_id}",
    response_model=ApplicationResponse
)
async def application_details(application_id: int, db_session: AsyncSession=Depends(get_db_session)) -> ApplicationResponse:
    application = await application.fetch_by_id(application_id, db_session)
    return ApplicationResponse.from_orm(application)


@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationBase, db_session: AsyncSession=Depends(get_db_session)) -> ApplicationResponse:
    application = await application.create(application, db_session)
    return ApplicationResponse.from_orm(application)
