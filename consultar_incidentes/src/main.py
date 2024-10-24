from fastapi import FastAPI, status, Depends
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from .database import database
from .models import models
from .tasks import tasks
from .utility import utility
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return RedirectResponse(url="/docs/")


@app.get("/incidentes", status_code=status.HTTP_200_OK)
def get(cliente: Optional[str] = None, usuario: Optional[str] = None, db: Session = Depends(database.get_db)):
    if cliente is None and usuario is None:
        incidentes = tasks.get(db=db)
    elif cliente is not None :
        incidentes = tasks.getIncidenteByCliente(db=db , client=cliente)
    else :
        incidentes = tasks.getIncidenteByUsuario(db=db , usuario=usuario)
    return [{
        "fechacreacion": incidente.fechacreacion,
        "correo": incidente.correo,
        "telefono": incidente.telefono,
        "descripcion": incidente.descripcion,
        "estado": incidente.estado,
        "id": incidente.id,
        "cliente": incidente.cliente_relacion,
        "usuario": incidente.usuario_relacion,
        "direccion": incidente.direccion,
        "prioridad": incidente.prioridad,
        "comentarios": incidente.comentarios
    } for incidente in incidentes]

@app.get("/incidente/{id}", status_code=status.HTTP_200_OK)
def get(id:int, db: Session = Depends(database.get_db)):
    incidente = tasks.getById(db=db, id=id)
    if not incidente:
        return utility.get_json_response('E404', 'La incidencia no existe') 
    return {
        "fechacreacion": incidente.fechacreacion,
        "correo": incidente.correo,
        "telefono": incidente.telefono,
        "descripcion": incidente.descripcion,
        "estado": incidente.estado,
        "id": incidente.id,
        "cliente": incidente.cliente_relacion,
        "usuario": incidente.usuario_relacion,
        "direccion": incidente.direccion,
        "prioridad": incidente.prioridad,
        "comentarios": incidente.comentarios
    } 

@app.get("/incidentes/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.delete("/incidentes/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db(db=db)
    return {"msg": "Todos los incidentes fueron eliminados"}
