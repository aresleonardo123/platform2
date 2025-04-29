from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ubicacion(BaseModel):
    lat: float
    lon: float
    fecha: str

@app.get("/", response_class=HTMLResponse)
def ver_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/guardar")
async def guardar_ubicacion(data: Ubicacion):
    with open("ubicaciones_gps.json", "a") as f:
        f.write(json.dumps(data.dict()) + "\n")
    return {"estado": "ok"}

@app.post("/guardar")
async def guardar_ubicacion(data: Ubicacion):
    print("Se recibió ubicación:", data.dict())  # 👈 Ver en consola
    with open("ubicaciones_gps.json", "a") as f:
        f.write(json.dumps(data.dict()) + "\n")
    return {"estado": "ok"}
from fastapi.responses import JSONResponse
import os

@app.get("/ver-ubicaciones")
def ver_ubicaciones():
    if os.path.exists("ubicaciones_gps.json"):
        with open("ubicaciones_gps.json", "r") as f:
            datos = [json.loads(line) for line in f if line.strip()]
        return JSONResponse(content=datos)
    else:
        return JSONResponse(content={"error": "Archivo no encontrado"}, status_code=404)
