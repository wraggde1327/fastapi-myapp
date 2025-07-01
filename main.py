from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional

app = FastAPI()

origins = [
    "https://wraggde1327.github.io",
    # "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_SCRIPT_BASE = "https://script.google.com/macros/s/AKfycbxi4lw0XyZs_Iuasr3T06Jfah-kO6PyaSY4qOLK6SolFZd2mmAxXo7ajcjqcJ2u6wM/exec"
GOOGLE_SCRIPT_PENDING_URL = f"{GOOGLE_SCRIPT_BASE}?action=getPending"
GOOGLE_SCRIPT_CLIENTS_URL = f"{GOOGLE_SCRIPT_BASE}?action=getClients"
GOOGLE_SCRIPT_POST_URL = GOOGLE_SCRIPT_BASE

class InvoiceUpdate(BaseModel):
    invoice_id: int
    amount: float
    who: str

class InvoiceCreate(BaseModel):
    id: int
    sum: float
    type: str
    who: str
    
class ContractCreate(BaseModel):
    contractNumber: str
    contractDate: str
    orgType: str
    zakazchik: str
    inn: str
    ogrn: str
    lico: str
    osnovan: str
    rucl: str
    adress: str
    tel: str = None
    pochta: str
    bank: str
    bik: str
    rs: str
    ks: str = None
    tarif: str
    who: str
    
@app.get("/pending")
async def get_pending():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
        async with httpx.AsyncClient() as client:
            response = await client.get(GOOGLE_SCRIPT_PENDING_URL, headers=headers, follow_redirects=True)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"Ошибка от Google Script: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/clients")
async def get_clients():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
        async with httpx.AsyncClient() as client:
            response = await client.get(GOOGLE_SCRIPT_CLIENTS_URL, headers=headers, follow_redirects=True)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"Ошибка от Google Script: {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/invoices")
async def create_invoice(invoice: InvoiceCreate):
    try:
        # Google Script ждет параметры через form-data или query, но если он поддерживает JSON — можно так:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_SCRIPT_POST_URL,
                json={"action": "createInvoice", **invoice.dict()},
                follow_redirects=True
            )
            response.raise_for_status()
            # Возвращаем ответ сервера Google Script (текст или JSON)
            try:
                return response.json()
            except Exception:
                return {"result": response.text}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка от Google Script: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update_invoice")
async def update_invoice(update: InvoiceUpdate):
    try:
        async with httpx.AsyncClient() as client:
            payload = update.dict()
            payload["action"] = "updateInvoice"
            response = await client.post(
                GOOGLE_SCRIPT_POST_URL,
                json=payload,
                follow_redirects=True
            )
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка от Google Script: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contracts")
async def create_contract(contract: ContractCreate):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_SCRIPT_POST_URL,
                json={"action": "createContract", **contract.dict()},
                follow_redirects=True
            )
            response.raise_for_status()
            try:
                return response.json()
            except Exception:
                return {"result": response.text}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка от Google Script: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

