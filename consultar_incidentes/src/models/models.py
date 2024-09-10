from sqlalchemy import BigInteger, Column, String, DateTime
from ..database import database


class Incidentes(database.Base):
    __tablename__ = "INCIDENTES"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    DESCRIPCION = Column(String)
    ESTADO = Column(String)
    FECHACREACION = Column(DateTime)
    GESTORABC = Column(String)
    CLIENTE = Column(String)
    USUARIO = Column(String)
    COMENTARIOS = Column(String)


database.Base.metadata.create_all(bind=database.engine)
