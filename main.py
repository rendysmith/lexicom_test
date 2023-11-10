# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import redis

class WriteDataRequest(BaseModel):
    phone: str
    address: str

tags_metadata = [
    {
        "name": "Health",
        "description": "Стартовая точка"
    }
]
app = FastAPI(openapi_url="/api/v1/openapi.json", docs_url='/swagger', openapi_tags=tags_metadata)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


@app.post("/write_data")
def write_data(request: WriteDataRequest):
    phone = request.phone
    address = request.address
    redis_client.set(phone, address)
    return JSONResponse(content={"message": "Data written successfully"})

@app.get("/check_data")
def check_data(phone: str):
    address = redis_client.get(phone)
    if address:
        return JSONResponse(content={"address": address})
    else:
        return JSONResponse(content={"message": "Address not found"}, status_code=404)