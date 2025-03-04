from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# Загрузка данных из файла parsed_data.json
def load_data():
    with open("backend/parsed_dash.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

@app.get("/data", response_class=JSONResponse)
async def get_data():
    data = load_data()
    # Возвращаем первые 15 объектов
    return data[:15]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

