from datetime import datetime
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def create(db: Session, incidente: schemas.Incidentes) -> models.Incidentes:
    date_format = '%Y-%m-%d %H:%M:%S'
    incidente = models.Incidentes(
        cliente=incidente.cliente.lower(),
        fechacreacion=datetime.strptime(incidente.fechacreacion, date_format),
        usuario=incidente.usuario.lower(),
        correo=incidente.correo.lower(),
        direccion=incidente.direccion.lower(),
        telefono=incidente.telefono.lower(),
        descripcion=incidente.descripcion.lower(),
        prioridad=incidente.prioridad.lower(),
        estado=incidente.estado.lower(),
        comentarios=incidente.comentarios.lower(),
    )
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
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
    )
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente


def reset_db(db: Session):
    db.query(models.Incidentes).delete()
    db.commit()
