from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Разрешаем CORS откуда угодно (или указать домен github.io)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["https://твойдомен.github.io"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec"

@app.get("/proxy")
async def proxy_get(action: str):
    """
    GET прокси — принимает параметр action,
    передает на Google Script и возвращает JSON.
    """
    params = {"action": action}
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(GOOGLE_SCRIPT_URL, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к Google Script: {e}")

@app.post("/proxy")
async def proxy_post(request: Request):
    """
    POST прокси — принимает JSON тело и
    пересылает на Google Script.
    """
    json_body = await request.json()
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(GOOGLE_SCRIPT_URL, json=json_body, timeout=10)
            r.raise_for_status()
            return r.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к Google Script: {e}")
