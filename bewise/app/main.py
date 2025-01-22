import uvicorn

from . import init_app

app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
