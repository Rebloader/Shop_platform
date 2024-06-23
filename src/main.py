import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {'project': 'shop api'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
    