from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import random
import string
import re
from pydantic import BaseModel
from utils import get_country_by_ip, get_client_ip

router = APIRouter()

@router.get("/start")
async def start(request: Request, mystical_word: str | None = None):
    ip = get_client_ip(request)
    
    # Проверяем страну для доступа к /start
    country = await get_country_by_ip(ip)
    
    print(f"Страна для IP {ip}: {country}")  # Отладочная информация
    
    # Если страна не Россия, возвращаем ошибку
    if country != "RU":
        return JSONResponse(
            content={"message": "Гуси не действуют на территории наших слонов."},
            status_code=403
        )
        
    if mystical_word is None:
        return {"msg": "Чтобы токен получить слово секретное нужно произносить. Это вам не загадки Вжака Каламбэска."}
    elif mystical_word.lower() == "слон": 
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
async def process_request(request: Request, token: str, body: RequestBody):
    ip = get_client_ip(request)
    
    # Проверяем страну для доступа к /token
    country = await get_country_by_ip(ip)
    
    print(f"Страна для IP {ip}: {country}")  # Отладочная информация
    
    # Если страна не Россия, возвращаем ошибку
    if country != "RU":
        return JSONResponse(
            content={"message": "Гуси не действуют на территории наших слонов."},
            status_code=403
        )
    
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
        "message": "Слон > гуся. Иди дальше га-гакай"
    }
