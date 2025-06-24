from fastapi import FastAPI
import httpx

app = FastAPI()

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec?action=getPending"

@app.get("/pending")
async def get_pending():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
        async with httpx.AsyncClient() as client:
            response = await client.get(GOOGLE_SCRIPT_URL, headers=headers, follow_redirects=True)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"Ошибка от Google Script: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}
