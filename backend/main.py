from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Загрузка данных из файла metrics_DB.json
def load_data():
    with open("metrics_DB.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

fakeDB = load_data()

@app.get("/data", response_class=JSONResponse)
async def get_data():
    return fakeDB

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

