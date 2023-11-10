# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import redis
from dotenv import load_dotenv
import os

class WriteDataRequest(BaseModel):
    phone: str
    address: str

app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url='/swagger')

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

host = os.environ.get("host")
port = os.environ.get("port")
db_name = os.environ.get("db_name")
db_pass = os.environ.get("db_pass")

redis_client = redis.StrictRedis(
    host=host,
    port=port,
    db=db_name,
    password=db_pass,
    decode_responses=True)

@app.post("/write_data", tags=['Data'])
def write_data(request: WriteDataRequest):
    """API для записи данных в БД (Телефон, Адрес)"""
    phone = request.phone
    address = request.address
    existing_address = redis_client.get(phone)
    if existing_address:
        redis_client.set(phone, address)
        return JSONResponse(content={"message": "Обновляем данные"})
    else:
        # Write new data
        redis_client.set(phone, address)
        return JSONResponse(content={"message": "Вносим новую запись"})

@app.get("/check_data", tags=['Data'])
def check_data(phone: str):
    """API для извлечения данных из БД согласно указанному телефону"""
    address = redis_client.get(phone)
    if address:
        return JSONResponse(content={"address": address})
    else:
        return JSONResponse(content={"message": "Адрес не найден, проверьте телефон на корректность"}, status_code=404)




