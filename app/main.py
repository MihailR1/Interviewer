from fastapi import FastAPI

from app.base.utils import datetime_now

app = FastAPI()


@app.get("/")
async def main():
    print(datetime_now())
    return None
