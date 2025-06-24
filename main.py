from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

origins = [
    "https://wraggde1327.github.io",
    # Или можно разрешить все, но осторожно:
    # "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_SCRIPT_GET_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec?action=getPending"
GOOGLE_SCRIPT_POST_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec"

class InvoiceUpdate(BaseModel):
    invoice_id: int
    amount: float

@app.get("/pending")
async def get_pending():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
        async with httpx.AsyncClient() as client:
            response = await client.get(GOOGLE_SCRIPT_GET_URL, headers=headers, follow_redirects=True)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"Ошибка от Google Script: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/update_invoice")
async def update_invoice(update: InvoiceUpdate):
    try:
        async with httpx.AsyncClient() as client:
            # Отправляем JSON как есть
            response = await client.post(
                GOOGLE_SCRIPT_POST_URL,
                json=update.dict(),
                follow_redirects=True
            )
            response.raise_for_status()
            # Возвращаем ответ сервера Google Script (текст или JSON)
            return response.text
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка от Google Script: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
