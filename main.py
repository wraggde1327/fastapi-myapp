from fastapi import FastAPI
import httpx

app = FastAPI()

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec"

@app.get("/get-pending")
async def get_pending():
    async with httpx.AsyncClient() as client:
        response = await client.get(GOOGLE_SCRIPT_URL, params={"action": "getPending"})
        response.raise_for_status()  # выбросит ошибку, если код ответа 4xx/5xx
        return response.json()
