from dotenv import find_dotenv, load_dotenv
from typing import TypedDict
from pydantic import NegativeInt
from sqlalchemy.orm import Session
from datetime import datetime

from ..models import models
from ..schemas import schemas
from ..utility import utility

env_file = find_dotenv('.env.usuarios')
loaded = load_dotenv(env_file)


class CreationUser(TypedDict):
    user: models.Usuarios
    token: str


def verify_if_user_already_exist(db: Session, username: str, email: str):
    user = db.query(models.Usuarios).filter((models.Usuarios.USERNAME == username)
                                            | (models.Usuarios.EMAIL == email)).first()
    return user if user else False


def verify_if_user_exist_by_email(db: Session, email: str):
    user = db.query(models.Usuarios).filter(models.Usuarios.EMAIL == email).first()
    return user if user else False


def get_access_token(email: str, username: str):
    return utility.generate_jwt(email, username)


def create_roles(db: Session, roles: list[str]):
    for rol in roles:
        isRolCreated = get_rol_by_nombre(db, rol.lower())
        if not isRolCreated:
            new_rol = models.Roles(NOMBRE=rol.lower())
            db.add(new_rol)
            db.commit()
            db.refresh(new_rol)
    roles_stored = get_all_roles(db)
    return roles_stored


def create_permisos(db: Session, permisos: list[str]):
    for permiso in permisos:
        isPermisoCreated = get_permiso_by_nombre(db, permiso.lower())
        if not isPermisoCreated:
            new_permiso = models.Permisos(NOMBRE=permiso.lower())
            db.add(new_permiso)
            db.commit()
            db.refresh(new_permiso)
    permisos_stored = get_all_permisos(db)
    return permisos_stored


def asociar_permisos_roles(db: Session, asociaciones: list[schemas.AsociacionPermisos]):
    for asociacion in asociaciones:
        rol = get_rol_by_id(db, asociacion.ROL_ID)
        permiso = get_permiso_by_id(db, asociacion.PERMISO_ID)
        if permiso not in rol.PERMISOS:
            rol.PERMISOS.append(permiso)
            db.commit()
            db.refresh(rol)
    roles_stored = get_all_roles(db)
    return [{"ID": thisRol.ID, "NOMBRE": thisRol.NOMBRE, "PERMISOS": thisRol.PERMISOS} for thisRol in roles_stored]


def get_all_roles(db: Session):
    roles = db.query(models.Roles).all()
    return roles if roles else False


def get_all_permisos(db: Session):
    permisos = db.query(models.Permisos).all()
    return permisos if permisos else False


def get_rol_by_id(db: Session, id: int) -> models.Roles:
    rol = db.query(models.Roles).filter(models.Roles.ID == id).first()
    return rol if rol else False


def get_rol_by_nombre(db: Session, nombre: str):
    rol = db.query(models.Roles).filter(models.Roles.NOMBRE == nombre).first()
    return rol if rol else False


def get_permiso_by_id(db: Session, id: int) -> models.Permisos:
    permiso = db.query(models.Permisos).filter(models.Permisos.ID == id).first()
    return permiso if permiso else False


def get_permiso_by_nombre(db: Session, nombre: str):
    permiso = db.query(models.Permisos).filter(models.Permisos.NOMBRE == nombre).first()
    return permiso if permiso else False


def create_user(db: Session, user: schemas.UserRegister, rol: models.Roles) -> CreationUser:
    access_token = get_access_token(email=user.email, username=user.username)
    hashed = utility.get_password_hash(user.password)
    today = datetime.today()
    new_user = models.Usuarios(
        EMAIL=user.email.lower(),
        USERNAME=user.username.lower(),
        TELEFONO=user.telefono.lower(),
        PASSWORD=hashed,
        NOMBRES=user.nombres.lower(),
        APELLIDOS=user.apellidos.lower(),
        DIRECCION=user.direccion.lower() if user.direccion else "",
        FECHACREACION=today,
        GESTORTIER=user.gestortier.lower() if user.gestortier else "junior",
    )
    new_user.ROLEID = rol.ID
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return dict(
        user=new_user,
        token=access_token,
    )


def authenticate_user_by_password(user: models.Usuarios, password: str):
    return utility.verify_password(password, user.PASSWORD) if True else False


def reset_db_users(db: Session):
    db.query(models.Usuarios).delete()
    db.commit()


def reset_db_roles_permisos(db: Session):
    db.query(models.Permisos).delete()
    db.query(models.Roles).delete()
    db.commit()
