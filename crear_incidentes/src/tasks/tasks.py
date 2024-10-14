from datetime import datetime
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def create(db: Session, incidente: schemas.Incidentes) -> models.Incidentes:
    date_format = '%Y-%m-%d %H:%M:%S'
    incidente = models.Incidentes(
        CLIENTE=incidente.cliente.lower(),
        FECHACREACION=datetime.strptime(incidente.fechacreacion, date_format),
        USUARIO=incidente.usuario.lower(),
        CORREO=incidente.correo.lower(),
        DIRECCION=incidente.direccion.lower(),
        TELEFONO=incidente.telefono.lower(),
        DESCRIPCION=incidente.descripcion.lower(),
        PRIORIDAD=incidente.prioridad.lower(),
        ESTADO=incidente.estado.lower(),
        COMENTARIOS=incidente.comentarios.lower(),
    )
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente


def reset_db(db: Session):
    db.query(models.Incidentes).delete()
    db.commit()
