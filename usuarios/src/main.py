from dotenv import find_dotenv, load_dotenv
from fastapi import Body, FastAPI, status, Depends, Header
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from operator import itemgetter

from sqlalchemy.orm import Session
from .schemas import schemas
from .tasks import tasks
from .database import database
from .utility import utility

env_file = find_dotenv('.env.usuarios')
loaded = load_dotenv(env_file)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return RedirectResponse(url="/docs/")


@app.get("/roles", status_code=status.HTTP_200_OK)
def getAllRoles(db: Session = Depends(database.get_db)):
    roles = tasks.get_all_roles(db=db)
    if not roles:
        return utility.get_json_response('E404', 'No hay roles creados')
    else:
        return [{"id": role.id, "nombre": role.nombre, "permisos": role.permisos} for role in roles]


@app.post("/roles/crear", status_code=status.HTTP_201_CREATED)
def create_roles(roles: list[str] = Body(default=None), db: Session = Depends(database.get_db)):
    if not roles:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        roles = tasks.create_roles(db, roles)
        return roles


@app.get("/permisos", status_code=status.HTTP_200_OK)
def getAllPermisos(db: Session = Depends(database.get_db)):
    permisos = tasks.get_all_permisos(db=db)
    if not permisos:
        return utility.get_json_response('E404', 'No hay permisos creados')
    else:
        return [{"id": permiso.id, "nombre": permiso.nombre, "roles": permiso.roles} for permiso in permisos]

@app.get("/usuarios", status_code=status.HTTP_200_OK)
def getAllUsuarios(db: Session = Depends(database.get_db)):
    usuarios = tasks.get_all_users(db=db)
    if not usuarios:
        return utility.get_json_response('E404', 'No hay usuarios creados')
    else:
        return [{
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "telefono": user.telefono,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
                "direccion": user.direccion,
                "fechacreacion": user.fechacreacion,
            } for user in usuarios]

@app.get("/usuarios/{role_id}", status_code=status.HTTP_200_OK)
def getAllUsuarios(role_id:int, db: Session = Depends(database.get_db)):
    usuarios = tasks.get_all_users_by_rol(db=db, role_id=role_id)
    if not usuarios:
        return utility.get_json_response('E404', 'No hay usuarios creados')
    else:
        return [{
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "telefono": user.telefono,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
                "direccion": user.direccion,
                "fechacreacion": user.fechacreacion,
            } for user in usuarios]


@app.post("/permisos/crear", status_code=status.HTTP_201_CREATED)
def create_permisos(permisos: list[str] = Body(default=None), db: Session = Depends(database.get_db)):
    if not permisos:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        permisos = tasks.create_permisos(db, permisos)
        return permisos


@app.post("/permisos/asociar/roles", status_code=status.HTTP_200_OK)
def asoaciar_permisos_roles(asociaciones: list[schemas.AsociacionPermisos] = Body(default=None), db: Session = Depends(database.get_db)):
    if not asociaciones:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        roles = tasks.asociar_permisos_roles(db, asociaciones)
        return roles


@app.post("/usuario/register", status_code=status.HTTP_201_CREATED)
def create_users(user: schemas.UserRegister = Body(default=None), db: Session = Depends(database.get_db)):
    rol = tasks.get_rol_by_id(db=db, id=user.rol)
    if not user:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not user.email or not user.username or not user.telefono or not user.password or not user.nombres or not user.apellidos or not user.rol:
        return utility.get_json_response('E400', 'email, username, telefono, password, nombres, apellidos y el rol son campos obligatorios')
    elif not rol:
        return utility.get_json_response('E404', 'el rol con este id no existe')
    else:
        email = user.email
        username = user.username
        user_db = tasks.verify_if_user_already_exist(db=db, email=email, username=username)
        if user_db:
            return utility.get_json_response('E412', 'Este usuario ya existe con este username y/o email')
        else:
            user, token = itemgetter('user', 'token')(tasks.create_user(db=db, user=user, rol=rol))
            isGestor: bool = rol.nombre == 'gestor'
            rol = tasks.get_rol_by_id(db=db, id=user.roleid)
            thisRol = {
                "id":  rol.id,
                "nombre": rol.nombre,
                "permisos": rol.permisos
            }
            returnData = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "telefono": user.telefono,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
                "direccion": user.direccion,
                "fechacreacion": user.fechacreacion,
                "token": token,
                "rol": thisRol,
            }
            if isGestor:
                returnData['gestortier'] = user.gestortier
            return returnData


@app.post("/usuario/login", status_code=status.HTTP_200_OK)
def login_users(user: schemas.UserLogin = Body(default=None), db: Session = Depends(database.get_db)):
    if not user:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not user.email or not user.password:
        return utility.get_json_response('E400', 'Email y password son campos obligatorios')
    else:
        email = user.email
        password = user.password
        user = tasks.verify_if_user_exist_by_email(db=db, email=email)
        if not user:
            return utility.get_json_response('E404', 'El usuario con este email no existe')
        else:
            is_authenticate = tasks.authenticate_user_by_password(user, password)
            if not is_authenticate:
                return utility.get_json_response('E401', 'Contraseña incorrecta')
            else:
                token = tasks.get_access_token(email=user.email, username=user.username)
                isGestor: bool = user.roleid == 3
                rol = tasks.get_rol_by_id(db=db, id=user.roleid)
                thisRol = {
                    "id":  rol.id,
                    "nombre": rol.nombre,
                    "permisos": rol.permisos
                }
                returnData = {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "telefono": user.telefono,
                    "nombres": user.nombres,
                    "apellidos": user.apellidos,
                    "direccion": user.direccion,
                    "fechacreacion": user.fechacreacion,
                    "token": token,
                    "rol": thisRol
                }
                if isGestor:
                    returnData['gestortier'] = user.gestortier
                return returnData


@app.get("/usuario/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "pong"}


@app.post("/usuario/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db_users(db=db)
    return {"msg": "Todos los usuarios fueron eliminados"}


@app.post("/rolesypermisos/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db_roles_permisos(db=db)
    return {"msg": "Todos los roles y permisos fueron eliminados"}
