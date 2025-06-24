from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec"

@app.get("/getPending")
async def get_pending():
    try:
        async with httpx.AsyncClient() as client:
            # Пример запроса с параметром action=getPending
            response = await client.get(GOOGLE_SCRIPT_URL, params={"action": "getPending"})
            response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Ошибка от Google Script: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
