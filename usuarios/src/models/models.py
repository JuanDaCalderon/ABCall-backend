import enum
import uuid
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, DateTime, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from ..database import database

roles_permisos = Table(
    'ROLES_PERMISOS', database.Base.metadata,
    Column('ROL_ID', BigInteger, ForeignKey('ROLES.ID', ondelete="CASCADE"), primary_key=True),
    Column('PERMISO_ID', BigInteger, ForeignKey('PERMISOS.ID', ondelete="CASCADE"), primary_key=True)
)


class GestorTiers(enum.Enum):
    junior = 'junior'
    mid = 'mid'
    senior = 'senior'
    lead = 'lead'
    manager = 'manager'


class Usuarios(database.Base):
    __tablename__ = "USUARIOS"
    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    EMAIL = Column(String, unique=True)
    USERNAME = Column(String, unique=True)
    TELEFONO = Column(String, unique=True)
    PASSWORD = Column(String)
    NOMBRES = Column(String)
    APELLIDOS = Column(String)
    DIRECCION = Column(String)
    FECHACREACION = Column(DateTime)
    GESTORTIER = Column(Enum(GestorTiers))
    ROLEID = mapped_column(ForeignKey("ROLES.ID", ondelete="CASCADE"))
    ROLES = relationship("Roles", back_populates="USUARIO")


class Roles(database.Base):
    __tablename__ = "ROLES"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    NOMBRE = Column(String, unique=True)
    USUARIO = relationship("Usuarios", back_populates="ROLES")
    PERMISOS = relationship("Permisos", secondary=roles_permisos, back_populates="ROLES")


class Permisos(database.Base):
    __tablename__ = "PERMISOS"
    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    NOMBRE = Column(String)
    ROLES = relationship("Roles", secondary=roles_permisos, back_populates="PERMISOS")


database.Base.metadata.create_all(bind=database.engine)
