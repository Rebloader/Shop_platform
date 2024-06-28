import uvicorn
from fastapi import FastAPI
from src.api_v1.views import router as api_router
from src.tasks.router import router as task_router
from src.api_v1.routers.dealers import router as dealers_router
from src.api_v1.routers.orders import router as orders_router
from src.api_v1.routers.provider import router as providers_router


app = FastAPI()
app.include_router(api_router)
app.include_router(task_router)
app.include_router(orders_router)
app.include_router(dealers_router)
app.include_router(providers_router)


@app.get("/")
async def root():
    return {'project': 'shop api'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
