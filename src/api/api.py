from fastapi import FastAPI, HTTPException
from czip import convert
from src.api.models.czip import InputData

app = FastAPI()


@app.get("/")
async def index():
    return "Welcome to CZip! Send a POST to /convert"


@app.post("/convert")
async def convert_data(input_data: InputData):
    try:
        result = convert(input_data.data)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
