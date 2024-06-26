import uvicorn
from fastapi import FastAPI
from src.api_v1.views import router as api_router
from src.tasks.router import router as task_router


app = FastAPI()
app.include_router(api_router)
app.include_router(task_router)


@app.get("/")
async def root():
    return {'project': 'shop api'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
