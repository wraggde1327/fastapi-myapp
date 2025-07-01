from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional
import logging

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

logger = logging.getLogger("uvicorn.error")

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
    tel: Optional[str] = None
    pochta: str
    bank: str
    bik: str
    rs: str
    ks: Optional[str] = None
    tarif: str
    who: str

# GET запросы оставляем без изменений, так как они не долгие
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

# Функции для фоновых задач
async def call_google_script_create_invoice(invoice: InvoiceCreate):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_SCRIPT_POST_URL,
                json={"action": "createInvoice", **invoice.dict()},
                follow_redirects=True
            )
            response.raise_for_status()
            logger.info(f"createInvoice response: {response.text}")
    except Exception as e:
        logger.error(f"Ошибка при вызове createInvoice: {e}")

async def call_google_script_update_invoice(update: InvoiceUpdate):
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
            logger.info(f"updateInvoice response: {response.text}")
    except Exception as e:
        logger.error(f"Ошибка при вызове updateInvoice: {e}")

async def call_google_script_create_contract(contract: ContractCreate):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_SCRIPT_POST_URL,
                json={"action": "createContract", **contract.dict()},
                follow_redirects=True
            )
            response.raise_for_status()
            logger.info(f"createContract response: {response.text}")
    except Exception as e:
        logger.error(f"Ошибка при вызове createContract: {e}")

# POST эндпоинты с BackgroundTasks
@app.post("/invoices")
async def create_invoice(invoice: InvoiceCreate, background_tasks: BackgroundTasks):
    background_tasks.add_task(call_google_script_create_invoice, invoice)
    return {"message": "Создание счет получено сервером, ожидаем выполнения в гугле"}

@app.post("/update_invoice")
async def update_invoice(update: InvoiceUpdate, background_tasks: BackgroundTasks):
    background_tasks.add_task(call_google_script_update_invoice, update)
    return {"message": "Проведение платежа получено сервером, ожидаем выполнения в гугле"}

@app.post("/contracts")
async def create_contract(contract: ContractCreate, background_tasks: BackgroundTasks):
    background_tasks.add_task(call_google_script_create_contract, contract)
    return {"message": "Договор получен сервером, ожидаем выполнения в гугле"}
