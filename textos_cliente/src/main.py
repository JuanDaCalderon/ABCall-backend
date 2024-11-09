from dotenv import find_dotenv, load_dotenv
from fastapi import Body, FastAPI, status, Depends, Header
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from operator import itemgetter

from sqlalchemy.orm import Session
from .schemas import schemas
from .tasks import tasks
from .database import database
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

@app.get("/texto/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "pong"}

@app.get("/texto", status_code=status.HTTP_200_OK)
def getAllTextos(db: Session = Depends(database.get_db)):
    textos = tasks.get_all_textos(db=db)
    if not textos:
        return utility.get_json_response('E404', 'No hay Textos creados')
    else:
        return [{"id": texto.id, "saludo": texto.saludo, "cierre": texto.cierre, "cliente": texto.usuario} for texto in textos]


@app.post("/texto", status_code=status.HTTP_201_CREATED)
def create_texto(texto: schemas.texto = Body(default=None), db: Session = Depends(database.get_db)):
    if not texto:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        texto = tasks.create_texto(db, texto)
        return texto

@app.get("/texto/{texto_id}", status_code=status.HTTP_200_OK)
def getTextoById(texto_id:int, db: Session = Depends(database.get_db)):
    texto = tasks.get_textos_by_id(db=db, id=texto_id)
    if not texto:
        return utility.get_json_response('E404', 'Texto no Existe')
    else:
        return {
                "id": texto.id,
                "saludo": texto.saludo,
                "cierre": texto.cierre,
                "cliente": texto.usuario,
            } 

@app.put("/texto", status_code=status.HTTP_200_OK)
def updateTexto( texto: schemas.textoUpdate = Body(default=None),db: Session = Depends(database.get_db)):
    if not texto:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        texto = tasks.update_textos(db, texto)
        return texto
@app.post("/texto/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db_textos(db=db)
    return {"msg": "Todos los textos fueron eliminados"}

