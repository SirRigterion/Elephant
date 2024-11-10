import aiohttp
from fastapi import Request
from typing import Optional


# Асинхронная функция для определения страны по IP-адресу через API IPInfo
async def get_country_by_ip(ip: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://ipinfo.io/{ip}/json") as response:
                data = await response.json()
                print(f"Ответ от IPInfo для IP {ip}: {data}")  # Отладочная информация
                return data.get("country", "")
    except Exception as e:
        print(f"Ошибка при получении данных о геолокации: {e}")
        return ""


# Функция для получения IP пользователя, учитывая прокси
def get_client_ip(request: Request) -> str:
    ip = request.client.host
    if "X-Forwarded-For" in request.headers:
        ip = request.headers.get("X-Forwarded-For").split(",")[0]
    return ip
