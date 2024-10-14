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
    elif not incidente.descripcion or not incidente.estado or not incidente.fechacreacion or not incidente.cliente or not incidente.usuario or not incidente.comentarios:
        return utility.get_json_response('E400', 'Todos los campos son obligatorios')
    else:
        new_incidente: models.Incidentes = tasks.create(db=db, incidente=incidente)
        return {
            "ID": new_incidente.ID,
            "CLIENTE": new_incidente.CLIENTE,
            "FECHACREACION": new_incidente.FECHACREACION,
            "USUARIO": new_incidente.USUARIO,
            "CORREO": new_incidente.CORREO,
            "DIRECCION": new_incidente.DIRECCION,
            "TELEFONO": new_incidente.TELEFONO,
            "DESCRIPCION": new_incidente.DESCRIPCION,
            "PRIORIDAD": new_incidente.PRIORIDAD,
            "ESTADO": new_incidente.ESTADO,
            "COMENTARIOS": new_incidente.COMENTARIOS,
        }


@app.get("/incidentes/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.delete("/incidentes/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db(db=db)
    return {"msg": "Todos los incidentes fueron eliminados"}
