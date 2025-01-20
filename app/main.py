import uvicorn

from fastapi import FastAPI

from app.api.routers.application import router as application_router

app = FastAPI(title="BeWise HomeAssignment")

@app.get("/")
async def root():
    return {"message": "BeWise HomeAssignment"}

app.include_router(application_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)