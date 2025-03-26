import base64
import datetime
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from l.rediscli import get_redis_client







@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.pool.close()


def get_application(prefix=None) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_application()


def get_pool() -> Pool:
    return app.state.pool


class LesTlakMsgModel(BaseModel):
    text: str
    time: str
    crawl_time: datetime.datetime = datetime.datetime.now()
    # img: str # base64


class SignTGDevModel(BaseModel):
    phone: str
    code: str
    # img: str # base64


class ImageMsgModel(BaseModel):
    img: str
    id: str
    time: datetime.datetime = datetime.datetime.now()


class PhoneModel(BaseModel):
    phone: str


@app.post("/app/endpoint")
async def method_name(data: LesTlakMsgModel, Depends=Depends(get_pool)):
    data.crawl_time = datetime.datetime.now()
    pool = get_pool()
    async with pool.acquire() as connection:
        async with connection.transaction():
            # TODO use third party library to import sql from sql file
            await connection.execute(
                """ INSERT into letstalk VALUES(default, $1, $2 , $3);""",
                data.time,
                data.crawl_time,
                data.text,
            )


def decode_base64_to_png(base64_string, output_path):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)

        # Write the binary data to a file
        with open(output_path, "wb") as file:
            file.write(image_data)

        print(f"Image successfully decoded and saved to {output_path}")
    except Exception as e:
        print(f"Error decoding base64 to PNG: {str(e)}")


@app.post("/app/decode_image")
async def decode_image(data: ImageMsgModel):
    print(data.img)
    if data.img:
        output_path = f"decoded_image_{data.id}{data.time}.png"
        decode_base64_to_png(data.img, output_path)
        return {"message": f"Image decoded and saved as {output_path}"}
    else:
        return {"error": "No image data provided"}


@app.post("/app/signuptgdev")
def signup_tg_dev(token: SignTGDevModel):
    print(token.phone)
    print(token.code)
    redis_cli = get_redis_client()
    redis_cli.set(token.phone, token.code)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")
