from dotenv import find_dotenv, load_dotenv

from typing import TypedDict

from sqlalchemy.orm import Session

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


def verify_if_user_already_exist_recovery(db: Session, username: str, email: str):
    user = db.query(models.Usuarios).filter((models.Usuarios.USERNAME == username)
                                            & (models.Usuarios.EMAIL == email)).first()
    return user if user else False

def verify_if_client_already_exist(db: Session, username: str, email: str):
    cliente = db.query(models.Cliente).filter((models.Cliente.NOMBRE == username)
                                            | (models.Cliente.EMAIL == email)).first()
    return cliente if cliente else False

def get_user_active(db: Session, username: str, email: str):
    user = db.query(models.Usuarios).filter((models.Usuarios.USERNAME == username)
                                            & (models.Usuarios.EMAIL == email)).first()
    return user if user else False


def verify_if_user_exist_by_email(db: Session, email: str):
    user = db.query(models.Usuarios).filter(models.Usuarios.EMAIL == email).first()
    return user if user else False


def get_access_token(email: str, username: str):
    return utility.generate_jwt(email, username)


def verify_token(token: str):
    return utility.verify_access_token(token=token)


def verify_token_has_expired(token: str):
    return utility.verify_if_token_has_expired(token=token)


def create_user(db: Session, user: schemas.UserRegister) -> CreationUser:
    access_token = get_access_token(email=user.email, username=user.username)
    hashed = utility.get_password_hash(user.password)
    new_user = models.Usuarios(
        EMAIL=user.email.lower(),
        USERNAME=user.username.lower(),
        NOMBRES=user.nombres.lower(),
        APELLIDOS=user.apellidos.lower(),
        PASSWORD=hashed,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return dict(
        user=new_user,
        token=access_token,
    )

def create_client(db:Session, client: schemas.ClienteRegister) -> schemas.ClienteResponse :
    new_client = models.Cliente( NOMBRE = client.nombre, EMAIL=client.email, TELEFONO = client.telefono, DIRECCION=client.direccion)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return dict(cliente = new_client)

def authenticate_user_by_password(user: models.Usuarios, password: str):
    return utility.verify_password(password, user.PASSWORD) if True else False


def check_user_with_id(db: Session, id: str, user: schemas.TokenObject):
    this_user = db.query(models.Usuarios).filter((models.Usuarios.ID == id) & (
        models.Usuarios.EMAIL == user['email']) & (models.Usuarios.USERNAME == user['username'])).first()
    if this_user:
        return True
    else:
        return False


def reset_db(db: Session):
    db.query(models.Usuarios).delete()
    db.commit()
