from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas

def get_all_textos(db: Session):
    textos = db.query(models.Textos).all()
    return textos if textos else False

def get_textos_by_id(db: Session, id:int):
    textos = db.query(models.Textos).filter(models.Textos.id== id).first()
    return textos if textos else False

def get_textos_by_idcliente(db: Session, idcliente:int):
    textos = db.query(models.Textos).filter(models.Textos.clienteid == idcliente).first()
    return textos if textos else False

def create_texto(db: Session, texto: schemas.texto) -> models.Textos:
    cliente:models.Usuarios = db.query(models.Usuarios).filter(models.Usuarios.id == texto.clienteid).first()
    new_texto = models.Textos(
        saludo=texto.saludo.lower(),
        cierre=texto.cierre.lower(),
        clienteid=cliente.id if cliente.id else "",
    )
    db.add(new_texto)
    db.commit()
    db.refresh(new_texto)
    return dict(texto=new_texto)

def update_textos(db:Session, texto: schemas.textoUpdate) -> models.Textos:
    textoUpdate = db.query(models.Textos).filter(models.Textos.id == texto.id).first()
    cliente:models.Usuarios = db.query(models.Usuarios).filter(models.Usuarios.id == texto.clienteid).first()
    textoUpdate.saludo = texto.saludo.lower()
    textoUpdate.cierre = texto.cierre.lower()
    textoUpdate.clienteid = cliente.id
    db.commit()
    db.refresh(textoUpdate)
    return dict(texto=textoUpdate)
def reset_db_textos(db: Session):
    db.query(models.Textos).delete()
    db.commit()
