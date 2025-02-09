from datetime import datetime
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def create(db: Session, incidente: schemas.Incidentes) -> models.Incidentes:
    gestor : models.Usuarios = db.query(models.Usuarios).filter(models.Usuarios.roleid == 3 and models.Usuarios.gestortier == 'junior').first()
    incidente = models.Incidentes(
        cliente=incidente.cliente,
        usuario=incidente.usuario,
        gestor = incidente.gestor if incidente.gestor != '' else gestor.id,
        correo=incidente.correo.lower(),
        direccion=incidente.direccion.lower(),
        telefono=incidente.telefono.lower(),
        descripcion=incidente.descripcion.lower(),
        prioridad=incidente.prioridad.lower(),
        estado=incidente.estado.lower(),
        comentarios=incidente.comentarios.lower(),
        canal = incidente.canal.lower(),
        tipo=incidente.tipo.lower(),
    )
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente

def editar(db: Session, incidente: schemas.Incidentes , id:int) -> models.Incidentes:
    incidente_edit : models.Incidentes = getById(db=db,id=id)
    incidente_edit.cliente = incidente.cliente
    incidente_edit.usuario = incidente.usuario
    incidente_edit.gestor = incidente.gestor
    incidente_edit.correo = incidente.correo
    incidente_edit.direccion = incidente.direccion
    incidente_edit.telefono = incidente.telefono
    incidente_edit.descripcion = incidente.descripcion
    incidente_edit.prioridad = incidente.prioridad
    incidente_edit.estado = incidente.estado
    incidente_edit.comentarios = incidente.comentarios
    incidente_edit.canal = incidente.canal
    incidente_edit.tipo = incidente.tipo
    db.commit()
    db.refresh(incidente_edit)
    return incidente_edit

def getById(db: Session , id:int) -> models.Incidentes:
    incidente: models.Incidentes = db.query(models.Incidentes).filter(models.Incidentes.id == id).first()
    return incidente

def createEmail(db: Session, incidente: schemas.IncidenteEmail) -> models.Incidentes:
    incidente = models.Incidentes(
        fechacreacion=datetime.today(),
        correo=incidente.correo.lower(),
        direccion=incidente.direccion.lower(),
        telefono=incidente.telefono.lower(),
        descripcion=incidente.descripcion.lower(),
        prioridad=incidente.prioridad.lower(),
        estado=incidente.estado.lower(),
        comentarios=incidente.comentarios.lower(),
        canal = incidente.canal.lower(),
        tipo=incidente.tipo.lower(),
    )
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente


def reset_db(db: Session):
    db.query(models.Incidentes).delete()
    db.commit()
