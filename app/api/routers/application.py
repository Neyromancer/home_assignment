from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.application import get_application_by_id, create_application
from app.schemas.application import ApplicationResponse, ApplicationBase


router = APIRouter(
    prefix="/api/applications",
    tags=["applications"],
    responses={404: {"description": "Not Found"}}
)

@router.get(
    "/applications/{application_id}",
    response_model=ApplicationResponse
)
async def get_application_by_id(application_id: int, db_session=None) -> ApplicationResponse:
    application = await get_applications(db_session)
    return ApplicationResponse.from_orm(application)


@router.post("/applications")
def create_application(application: Application, db_sessio: Session=None) -> ApplicationResponse:
    pass
