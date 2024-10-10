from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import database


class Role(database.Base):
    __tablename__ = "ROLE"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    NOMBRE = Column(String)
    PERMISOS = relationship("Permiso", back_populates="ROLE")
    

class Permiso(database.Base):
    __tablename__ = "PERMISO"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    NOMBRE = Column(String)
    ESTADO = Column(Boolean)
    ROLE_ID = Column(BigInteger, ForeignKey('ROLE.ID'))
    ROLE = relationship("Role", back_populates="PERMISOS")

database.Base.metadata.create_all(bind=database.engine)
