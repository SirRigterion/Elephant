from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from router import router
from utils import get_country_by_ip, get_client_ip

# Объявление App
app = FastAPI(
    title="Главный"
)

# Объявление роутеров
app.include_router(router)

# Зависимость для проверки страны пользователя
async def check_country(request: Request):
    ip = get_client_ip(request)
    
    # Получаем страну по IP
    country = await get_country_by_ip(ip)
    
    print(f"Страна для IP {ip}: {country}")  # Добавим отладочную информацию

    # Проверяем, что страна действительно "RU" (Россия)
    if country != "RU":  # Если страна не Россия
        raise HTTPException(
            status_code=403,
            detail="Гуси не действуют на территории наших слонов."
        )

# Маршрут для главной страницы
@app.get("/")
async def read_root(request: Request, _ = Depends(check_country)):
    return {"message": "Добро пожаловать!"}
