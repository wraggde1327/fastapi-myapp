from fastapi import FastAPI, Query
import httpx

app = FastAPI()

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec"

@app.get("/")
async def root():
    return {"message": "FastAPI работает 👍"}

@app.get("/getPending")
async def get_pending():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GOOGLE_SCRIPT_URL, params={"action": "getPending"})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"Ошибка при обращении к Google Script: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Произошла ошибка: {str(e)}"}
