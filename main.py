from fastapi import FastAPI, Depends
from pydantic import BaseModel
from src.config import Settings, get_settings
from src.yandex_gpt.YandexAgent import YandexAgent

app = FastAPI()

agent = YandexAgent()


@app.get("/info")
async def get_info(settings: Settings = Depends(get_settings)):
    return {"debug_mode": settings.debug, "port": settings.api_port}


@app.get("/")
async def root():
    return {"message": "hello world"}


class TextRequest(BaseModel):
    text: str


@app.post("/send-message")
async def process_text(request: TextRequest):
    answer = agent(request.text)
    return {"answer": answer}
