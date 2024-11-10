from fastapi import APIRouter, HTTPException
import random, string
from pydantic import BaseModel
import re


router = APIRouter()

@router.get("/start")
async def start(mystical_word: str | None = None):
    if mystical_word == None:
        return {"msg": "Чтобы токен получить слово секретное нужно произносить. Это вам не загадки Вжака Каламбэска."}
    elif mystical_word == "Слон" or mystical_word == "слон": 
        text_token = ''.join(random.sample(string.ascii_letters, 5)) + "-" + ''.join(random.sample(string.ascii_letters, 5))
        Token = f"biba-Gff-Tbbfr-Ybfre-{text_token}"
        return {"msg": Token}
    else:
        return {"msg": "Чтобы токен получить слово секретное нужно произносить. Это вам не загадки Вжака Каламбэска."}

# Модель для принятия JSON
class RequestBody(BaseModel):
    Our: str
    Tss: str

# Паттерн для проверки токена
TOKEN_PATTERN = r"^biba-Gff-Tbbfr\-Ybfre\-(.+)$"

@router.post("/token")
async def process_request(token: str, body: RequestBody):
    # Проверяем, что токен начинается с нужной части
    if not re.match(TOKEN_PATTERN, token):
        raise HTTPException(status_code=400, detail="Invalid token format")

    # Проверка на специальные значения в теле запроса
    if body.Our == "Elephant" and body.Tss == "Goose-Loser":
        invite_link = f"https://t.me/+csoIaGkIVBNhZGUy"
        # Уникальная ссылка на Telegram канал
        return {
            "message": "Вы настоящий слон",
            "telegram_channel": invite_link
        }
    
    # Если условия не соблюдены, просто возвращаем тело запроса и токен
    return {
        "message": "Request processed successfully",
        "token": token,
        "body": body.dict()
    }