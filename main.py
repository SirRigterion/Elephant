import aiohttp
import ipaddress
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from router import router

# Объявление App
app = FastAPI(
    title="Главный",
    docs_url=None  # Отключаем стандартную документацию
)

# Объявление роутеров
app.include_router(router)

# Асинхронная функция для определения страны по IP-адресу через API 2ip
async def get_country_by_ip(ip: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            # Запрос к API 2ip
            async with session.get(f"https://2ip.ru/api/geo/?ip={ip}") as response:
                data = await response.json()
                # Отладочная информация для анализа
                print(f"Ответ от 2ip для IP {ip}: {data}")
                country = data.get("country", "")
                return country
    except Exception as e:
        print(f"Ошибка при получении данных о геолокации: {e}")
        return ""

# Функция для получения IP пользователя, учитывая прокси
def get_client_ip(request: Request) -> str:
    ip = request.client.host
    if "X-Forwarded-For" in request.headers:
        ip = request.headers.get("X-Forwarded-For").split(",")[0]
    return ip

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

# Обработчик для документации /docs
@app.get("/docs", include_in_schema=False)
async def custom_docs(request: Request):
    ip = get_client_ip(request)
    
    # Проверяем страну для доступа к /docs
    country = await get_country_by_ip(ip)
    
    print(f"Страна для IP {ip}: {country}")  # Отладочная информация
    
    # Если страна не Россия, возвращаем ошибку
    if country != "RU":
        return JSONResponse(
            content={"message": "Гуси не действуют на территории наших слонов."},
            status_code=403
        )
    
    # Если страна Россия, возвращаем стандартную документацию
    return RedirectResponse(url='/docs')  # Это будет редиректить к документации FastAPI
