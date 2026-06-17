"""
TP01 - PP1 Python
API de Películas y Series con FastAPI

Esta API guarda los datos en un archivo JSON (data.json) para que
no se pierdan cuando se reinicia el servidor.

Endpoints:
    GET    /api/         -> lista todas las películas/series
    GET    /api/{id}      -> detalle de una película/serie por id
    POST   /api/          -> crea una nueva película/serie
    PUT    /api/{id}      -> edita una película/serie existente
    DELETE /api/{id}      -> elimina una película/serie
"""

import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------------------------------------------------
# Configuración de la app
# -----------------------------------------------------------------

app = FastAPI(title="API de Películas y Series - TP01")

# CORS: permite que el frontend (index.html abierto en el navegador)
# pueda hacer peticiones a esta API sin que el navegador las bloquee.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "data.json"


# -----------------------------------------------------------------
# Modelo de datos (Pydantic)
# -----------------------------------------------------------------

class Pelicula(BaseModel):
    titulo: str
    genero: str
    anio: int
    sinopsis: str
    imagen: Optional[str] = None


class PeliculaUpdate(BaseModel):
    """Igual que Pelicula pero todos los campos son opcionales,
    para poder editar solo algunos campos con PUT."""
    titulo: Optional[str] = None
    genero: Optional[str] = None
    anio: Optional[int] = None
    sinopsis: Optional[str] = None
    imagen: Optional[str] = None


# -----------------------------------------------------------------
# Funciones helper para leer / escribir el archivo JSON
# -----------------------------------------------------------------

def leer_datos() -> list:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos: list) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def obtener_siguiente_id(datos: list) -> int:
    if not datos:
        return 1
    return max(item["id"] for item in datos) + 1


# -----------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------

@app.get("/")
def home():
    """Ruta simple para confirmar que el servidor está vivo."""
    return {"mensaje": "API de Películas funcionando. Ir a /docs para probarla."}


@app.get("/api/")
def listar_peliculas():
    """Devuelve todas las películas/series guardadas."""
    return leer_datos()


@app.get("/api/{pelicula_id}")
def obtener_pelicula(pelicula_id: int):
    """Devuelve el detalle de una película/serie por su id."""
    datos = leer_datos()
    for pelicula in datos:
        if pelicula["id"] == pelicula_id:
            return pelicula
    raise HTTPException(status_code=404, detail="Película no encontrada")


@app.post("/api/", status_code=201)
def crear_pelicula(pelicula: Pelicula):
    """Crea una nueva película/serie."""
    datos = leer_datos()
    nueva = pelicula.model_dump()
    nueva["id"] = obtener_siguiente_id(datos)
    datos.append(nueva)
    guardar_datos(datos)
    return nueva


@app.put("/api/{pelicula_id}")
def editar_pelicula(pelicula_id: int, cambios: PeliculaUpdate):
    """Edita una película/serie existente. Solo actualiza los campos enviados."""
    datos = leer_datos()
    for pelicula in datos:
        if pelicula["id"] == pelicula_id:
            cambios_dict = cambios.model_dump(exclude_unset=True)
            pelicula.update(cambios_dict)
            guardar_datos(datos)
            return pelicula
    raise HTTPException(status_code=404, detail="Película no encontrada")


@app.delete("/api/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int):
    """Elimina una película/serie por id."""
    datos = leer_datos()
    nuevos_datos = [p for p in datos if p["id"] != pelicula_id]
    if len(nuevos_datos) == len(datos):
        raise HTTPException(status_code=404, detail="Película no encontrada")
    guardar_datos(nuevos_datos)
    return {"mensaje": f"Película con id {pelicula_id} eliminada"}
