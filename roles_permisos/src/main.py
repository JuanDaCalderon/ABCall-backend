from typing import List
from fastapi import Body, FastAPI, status, Depends
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from operator import itemgetter
from .database import database
from .models import models
from .schemas import schemas
from .tasks import tasks
from .utility import utility

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
    roles:List[models.Role] = tasks.findAllRoles(db=db)
    if not roles:
        return utility.get_json_response('E404', 'No hay roles creados') 
    else:
        return [{"ID":new_role.ID,"NOMBRE":new_role.NOMBRE,"PERMISOS":new_role.PERMISOS} for new_role in roles]

@app.get("/role/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.get("/role/{role_id}", status_code=status.HTTP_200_OK)
def getRole(role_id:int, db: Session = Depends(database.get_db)):
    new_role:models.Roles = tasks.findRoleById(db=db,role_id=role_id)
    if not new_role:
        return utility.get_json_response('E404', 'El role no existe') 
    else:
        return {
            "ID":new_role.ID,
            "NOMBRE":new_role.NOMBRE,
            "PERMISOS":new_role.PERMISOS
        }

@app.post("/role", status_code=status.HTTP_201_CREATED)
def create(role: schemas.role = Body(default=None), db: Session = Depends(database.get_db)):
    if not role:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not role.NOMBRE:
        return utility.get_json_response('E400', 'El nombre es obligatorio')
    
    new_role1:models.Roles = tasks.findRoleByName(db=db,role_name=role.NOMBRE)
    if new_role1:
        return utility.get_json_response('E400', 'El Role ya existe')
    else:
        new_role: models.Roles = tasks.createRole(db=db, role=role)
        return {
            "ID": new_role.ID,
            "NOMBRE": new_role.NOMBRE
        }

@app.post("/permiso", status_code=status.HTTP_201_CREATED)
def create(permiso: schemas.permiso = Body(default=None), db: Session = Depends(database.get_db)):
    if not permiso:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not permiso.NOMBRE or not permiso.ESTADO:
        return utility.get_json_response('E400', 'El nombre y el estado es obligatorio')
    
    new_permiso1:models.Permisos = tasks.findPermisoByName(db=db,permiso_name=permiso.NOMBRE)
    if new_permiso1:
        return utility.get_json_response('E400', 'El Permiso ya existe')
    else:
        new_permiso: models.Permisos = tasks.createPermiso(db=db, permiso=permiso)
        return {
            "ID": new_permiso.ID,
            "NOMBRE": new_permiso.NOMBRE
        }

@app.post("/role/{role_id}/permiso" , status_code=status.HTTP_201_CREATED)
def associate_permiso_to_role(role_id:int, permisos: schemas.PermisoUpdate = Body(default=None) , db: Session = Depends(database.get_db)):
    role:models.Roles = tasks.findRoleById(db=db,role_id=role_id)
    if not role:
        return utility.get_json_response('E404', 'El rol no existe')
    elif not permisos:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        new_role_permisos = itemgetter('role') (tasks.associatePermisosToRole(db=db, role=role, permisos=permisos))
        return {
            "ID": new_role_permisos.ID,
            "NOMBRE":new_role_permisos.NOMBRE,
            "PERMISOS":new_role_permisos.PERMISOS
            }



@app.delete("/role/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db(db=db)
    return {"msg": "Todos los roles y permisos fueron eliminados"}
