from fastapi import FastAPI

from app.base.utils import datetime_now

app = FastAPI()


@app.get("/")
async def main() -> None:
    print(datetime_now())
    return None
