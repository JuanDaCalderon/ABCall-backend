import enum
import uuid
from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey, Table, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from ..database import database

roles_permisos = Table(
    'ROLES_PERMISOS', database.Base.metadata,
    Column('rol_id', BigInteger, ForeignKey('ROLES.id', ondelete="CASCADE"), primary_key=True),
    Column('permiso_id', BigInteger, ForeignKey('PERMISOS.id', ondelete="CASCADE"), primary_key=True)
)


class GestorTiers(enum.Enum):
    junior = 'junior'
    mid = 'mid'
    senior = 'senior'
    lead = 'lead'
    manager = 'manager'


class Usuarios(database.Base):
    __tablename__ = "USUARIOS"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    telefono = Column(String, unique=True)
    password = Column(String)
    nombres = Column(String)
    apellidos = Column(String)
    direccion = Column(String)
    fechacreacion = Column(DateTime)
    gestortier = Column(Enum(GestorTiers))
    roleid = mapped_column(ForeignKey("ROLES.id", ondelete="CASCADE"))
    roles = relationship("Roles", back_populates="usuario")


class Roles(database.Base):
    __tablename__ = "ROLES"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True)
    usuario = relationship("Usuarios", back_populates="roles")
    permisos = relationship("Permisos", secondary=roles_permisos, back_populates="roles")


class Permisos(database.Base):
    __tablename__ = "PERMISOS"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True)
    roles = relationship("Roles", secondary=roles_permisos, back_populates="permisos")

    
database.Base.metadata.create_all(bind=database.engine)
