from sqlalchemy import BigInteger, Column, String, DateTime
from ..database import database


class Incidentes(database.Base):
    __tablename__ = "INCIDENTES"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente = Column(String) # mapped_column(ForeignKey("USUARIOS.id", ondelete="CASCADE"))
    fechacreacion = Column(DateTime)
    usuario = Column(String) # mapped_column(ForeignKey("USUARIOS.id", ondelete="CASCADE"))
    correo = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    descripcion = Column(String)
    prioridad = Column(String)
    estado = Column(String)
    COMENTARIOS = Column(String)
    
database.Base.metadata.create_all(bind=database.engine)
