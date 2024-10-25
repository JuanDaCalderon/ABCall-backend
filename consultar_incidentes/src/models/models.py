import enum
import uuid
from sqlalchemy import BigInteger, Column, String, DateTime , ForeignKey, DateTime, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from ..database import database


class Incidentes(database.Base):
    __tablename__ = "INCIDENTES"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cliente = Column(UUID(as_uuid=True), ForeignKey("USUARIOS.id", ondelete="CASCADE"))
    fechacreacion = Column(DateTime)
    usuario = Column(UUID(as_uuid=True), ForeignKey("USUARIOS.id", ondelete="CASCADE"))
    correo = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    descripcion = Column(String)
    prioridad = Column(String)
    estado = Column(String)
    comentarios = Column(String)
    canal = Column(String)
    tipo = Column(String)
    cliente_relacion = relationship("Usuarios", foreign_keys=[cliente], backref="incidentes_cliente")
    usuario_relacion = relationship("Usuarios", foreign_keys=[usuario], backref="incidentes_usuario")


class GestorTiers(enum.Enum):
    junior = 'junior'
    mid = 'mid'
    senior = 'senior'
    lead = 'lead'
    manager = 'manager'

roles_permisos = Table(
    'ROLES_PERMISOS', database.Base.metadata,
    Column('rol_id', BigInteger, ForeignKey('ROLES.id', ondelete="CASCADE"), primary_key=True),
    Column('permiso_id', BigInteger, ForeignKey('PERMISOS.id', ondelete="CASCADE"), primary_key=True)
)
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
