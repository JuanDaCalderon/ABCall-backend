from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def createRole(db: Session, role: schemas.role) -> models.Role:
    role = models.Role(
        NOMBRE=role.nombre.lower(),
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def findRoleByName(db: Session, role_name: schemas.role)->models.Role:
    role = db.query(models.Role).filter(models.Role.NOMBRE == role_name.lower()).first()
    return role if role else False

def findRoleById(db: Session, role_id: schemas.role)->models.Role:
    role = db.query(models.Role).filter(models.Role.ID == role_id).first()
    return role if role else False

def createPermiso(db: Session, permiso: schemas.permiso) -> models.Permiso:
    permiso = models.Permiso(
        NOMBRE=permiso.nombre.lower(),
        ESTADO=permiso.estado
    )
    db.add(permiso)
    db.commit()
    db.refresh(permiso)
    return permiso

def findPermisoByName(db: Session, permiso_name: schemas.role)->models.Role:
    permiso = db.query(models.Permiso).filter(models.Permiso.NOMBRE == permiso_name.lower()).first()
    return permiso if permiso else False

def findPermisoById(db: Session, permiso_id:int)->models.Role:
    permiso = db.query(models.Permiso).filter(models.Permiso.ID == permiso_id).first()
    return permiso if permiso else False

def associatePermisosToRole(db: Session,role: models.Role, permisos: schemas.PermisoUpdate) -> models.Role:
    for permiso_data in permisos.permisos:
        permiso = findPermisoById(db=db,permiso_id=permiso_data.id)
        permiso.ROLE_ID = role.ID
        db.add(permiso)  
        
    db.commit()
    db.refresh(role)
    return dict(role = role)

def reset_db(db: Session):
    db.query(models.Role).delete()
    db.query(models.Permiso).delete()
    db.commit()
