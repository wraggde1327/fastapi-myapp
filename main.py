from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
async def handle_action(action: str = None):
    if action == "getPending":
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://script.google.com/macros/s/AKfycbym6IzSkaOh6ekkBtSyJn_n8YWFYL17G3HPoFMSDURta3kzSLrMut92qFs9IUJQfxrm0Q/exec?action=getPending"
            )
        return r.text
    return {"error": "Invalid action"}
