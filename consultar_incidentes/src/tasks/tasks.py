from typing import List
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas

def get(db: Session) -> List[models.Incidentes]:
    incidentes: List[models.Incidentes] = db.query(models.Incidentes).all()
    return incidentes

def getById(db: Session , id:int) -> List[models.Incidentes]:
    incidente: models.Incidentes = db.query(models.Incidentes).filter(models.Incidentes.id == id).first()
    return incidente

def getIncidenteByCliente(db: Session, client:str):
    incidentes: List[models.Incidentes] = db.query(models.Incidentes).filter(models.Incidentes.cliente == client).all()
    return incidentes 

def getIncidenteByUsuario(db: Session, usuario:str):
    incidentes: List[models.Incidentes] = db.query(models.Incidentes).filter(models.Incidentes.usuario == usuario).all()
    return incidentes 
def reset_db(db: Session):
    db.query(models.Incidentes).delete()
    db.commit()
