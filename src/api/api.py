from fastapi import FastAPI, HTTPException
from czip import convert
from src.czip.currency_conversion import when_when_is_none
from src.api.models.czip import InputData

app = FastAPI()


@app.get("/")
async def index():
    return "Welcome to CZip! Send a POST to /convert"


@app.post("/convert")
async def convert_data(input_data: InputData):
    try:
        currency_string = input_data.currency
        when = input_data.when if input_data.when else when_when_is_none()
        result = convert(currency_string, when)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
