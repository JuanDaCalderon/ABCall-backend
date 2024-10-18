from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas


def createRole(db: Session, role: schemas.role) -> models.Roles:
    role = models.Roles(
        NOMBRE=role.NOMBRE.lower(),
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def findRoleByName(db: Session, role_name: schemas.role)->models.Roles:
    role = db.query(models.Roles).filter(models.Roles.NOMBRE == role_name.lower()).first()
    return role if role else False

def findRoleById(db: Session, role_id: schemas.role)->models.Roles:
    role = db.query(models.Roles).filter(models.Roles.ID == role_id).first()
    return role if role else False

def findAllRoles(db: Session):
    roles = db.query(models.Roles).all()
    return roles if roles else False
def createPermiso(db: Session, permiso: schemas.permiso) -> models.Permisos:
    permiso = models.Permisos(
        NOMBRE=permiso.NOMBRE.lower(),
        ESTADO=permiso.ESTADO
    )
    db.add(permiso)
    db.commit()
    db.refresh(permiso)
    return permiso

def findPermisoByName(db: Session, permiso_name: schemas.role)->models.Roles:
    permiso = db.query(models.Permisos).filter(models.Permisos.NOMBRE == permiso_name.lower()).first()
    return permiso if permiso else False

def findPermisoById(db: Session, permiso_id:int)->models.Roles:
    permiso = db.query(models.Permisos).filter(models.Permisos.ID == permiso_id).first()
    return permiso if permiso else False

def associatePermisosToRole(db: Session,role: models.Roles, permisos: schemas.PermisoUpdate) -> models.Roles:
    print(permisos.PERMISOS[0].ID) 
    for permiso_data in permisos.PERMISOS:
        permiso = findPermisoById(db=db,permiso_id=permiso_data.ID)
        if permiso not in role.PERMISOS:
            role.PERMISOS.append(permiso) 
        
    db.commit()
    db.refresh(role)
    return dict(role = role)

def reset_db(db: Session):
    db.query(models.Roles).delete()
    db.query(models.Permisos).delete()
    db.commit()
