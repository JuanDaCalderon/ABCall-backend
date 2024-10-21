from sqlalchemy import BigInteger, Column, String, DateTime
from ..database import database


class Incidentes(database.Base):
    __tablename__ = "INCIDENTES"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    CLIENTE = Column(String)
    FECHACREACION = Column(DateTime)
    USUARIO = Column(String)
    CORREO = Column(String)
    DIRECCION = Column(String)
    TELEFONO = Column(String)
    DESCRIPCION = Column(String)
    PRIORIDAD = Column(String)
    ESTADO = Column(String)
    COMENTARIOS = Column(String)

database.Base.metadata.create_all(bind=database.engine)
