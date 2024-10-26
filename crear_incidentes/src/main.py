from fastapi import Body, FastAPI, status, Depends
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import database
from .models import models
from .schemas import schemas
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


@app.post("/incidentes", status_code=status.HTTP_201_CREATED)
def create(incidente: schemas.Incidentes = Body(default=None), db: Session = Depends(database.get_db)):
    if not incidente:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not incidente.descripcion or not incidente.estado or not incidente.cliente or not incidente.usuario or not incidente.comentarios:
        return utility.get_json_response('E400', 'Todos los campos son obligatorios')
    else:
        new_incidente: models.Incidentes = tasks.create(db=db, incidente=incidente)
        return {
            "id": new_incidente.id,
            "cliente": new_incidente.cliente,
            "fechacreacion": new_incidente.fechacreacion,
            "usuario": new_incidente.usuario,
            "gestor": new_incidente.gestor,
            "correo": new_incidente.correo,
            "direccion": new_incidente.direccion,
            "telefono": new_incidente.telefono,
            "descripcion": new_incidente.descripcion,
            "prioridad": new_incidente.prioridad,
            "estado": new_incidente.estado,
            "comentarios": new_incidente.comentarios,
            "canal": new_incidente.canal,
            "tipo": new_incidente.tipo
        }

@app.put("/incidentes/{id}", status_code=status.HTTP_201_CREATED)
def edit(id:int, incidente: schemas.Incidentes = Body(default=None), db: Session = Depends(database.get_db)):
    incidenteEdit = tasks.getById(db=db, id=id)
    if not incidente:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not incidente.descripcion or not incidente.estado or not incidente.cliente or not incidente.usuario or not incidente.comentarios:
        return utility.get_json_response('E400', 'Todos los campos son obligatorios')
    elif not incidenteEdit :
        return utility.get_json_response('E404', 'El incidente no existe')
    else:
        new_incidente: models.Incidentes = tasks.editar(db=db, incidente=incidente , id=id)
        return {
            "id": new_incidente.id,
            "cliente": new_incidente.cliente,
            "usuario": new_incidente.usuario,
            "gestor": new_incidente.gestor,
            "fechacreacion": new_incidente.fechacreacion,
            "correo": new_incidente.correo,
            "direccion": new_incidente.direccion,
            "telefono": new_incidente.telefono,
            "descripcion": new_incidente.descripcion,
            "prioridad": new_incidente.prioridad,
            "estado": new_incidente.estado,
            "comentarios": new_incidente.comentarios,
            "canal": new_incidente.canal,
            "tipo": new_incidente.tipo
        }

@app.post("/incidente/email", status_code=status.HTTP_201_CREATED)
def createEmail(incidente: schemas.IncidenteEmail = Body(default=None), db: Session = Depends(database.get_db)):
    if not incidente:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not incidente.descripcion or not incidente.estado or not incidente.comentarios:
        return utility.get_json_response('E400', 'Todos los campos son obligatorios')
    else:
        new_incidente: models.Incidentes = tasks.createEmail(db=db, incidente=incidente)
        return {
            "id": new_incidente.id,
            "cliente": new_incidente.cliente,
            "fechacreacion": new_incidente.fechacreacion,
            "usuario": new_incidente.usuario,
            "gestor": new_incidente.gestor,
            "correo": new_incidente.correo,
            "direccion": new_incidente.direccion,
            "telefono": new_incidente.telefono,
            "descripcion": new_incidente.descripcion,
            "prioridad": new_incidente.prioridad,
            "estado": new_incidente.estado,
            "comentarios": new_incidente.comentarios,
            "canal": new_incidente.canal,
            "tipo": new_incidente.tipo
        }


@app.get("/incidentes/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.delete("/incidentes/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db(db=db)
    return {"msg": "Todos los incidentes fueron eliminados"}
