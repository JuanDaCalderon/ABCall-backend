from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import database


role_permiso = Table(
    'ROLE_PERMISO', database.Base.metadata,
    Column('ROLE_ID', BigInteger, ForeignKey('ROLE.ID'), primary_key=True),
    Column('PERMISO_ID', BigInteger, ForeignKey('PERMISO.ID'), primary_key=True)
)

class Permiso(database.Base):
    __tablename__ = "PERMISO"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    NOMBRE = Column(String)
    ESTADO = Column(Boolean)
    ROLES = relationship("Role", secondary=role_permiso, back_populates="PERMISOS")

class Role(database.Base):
    __tablename__ = "ROLE"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    NOMBRE = Column(String)
    PERMISOS = relationship("Permiso", secondary=role_permiso, back_populates="ROLES")
    
    
database.Base.metadata.create_all(bind=database.engine)
