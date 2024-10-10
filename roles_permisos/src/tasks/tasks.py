from datetime import datetime
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def createRole(db: Session, role: schemas.role) -> models.Role:
    role = models.role(
        NOMBRE=role.nombre.lower(),
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def findRoleByName(db: Session, role_name: schemas.role)->models.Role:
    role = db.query(models.Role).filter(models.Role.NOMBRE == role_name).first()
    return role
def createPermiso(db: Session, permiso: schemas.permiso) -> models.Permiso:
    permiso = models.Permiso(
        NOMBRE=permiso.nombre.lower(),
        ESTADO=permiso.estado
    )
    db.add(permiso)
    db.commit()
    db.refresh(permiso)
    return permiso

def associatePermisosToRole(db: Session,role: schemas.role, permisos: schemas.PermisoUpdate) -> models.Role:
    role.permisos = permisos
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def reset_db(db: Session):
    db.query(models.Role).delete()
    db.query(models.Permiso).delete()
    db.commit()
