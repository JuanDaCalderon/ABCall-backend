from fastapi import Body, FastAPI, status, Depends
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
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


@app.post("/role", status_code=status.HTTP_201_CREATED)
def create(role: schemas.role = Body(default=None), db: Session = Depends(database.get_db)):
    if not role:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not role.nombre:
        return utility.get_json_response('E400', 'El nombre es obligatorio')
    else:
        new_role1:models.Role = tasks.findRoleByName(db=db,role_name=role.nombre)
        if not new_role1:
            return utility.get_json_response('E400', 'El Role ya existe')
        
        new_role: models.Role = tasks.createRole(db=db, role=role)
        return {
            "ID": new_role.ID,
            "NOMBRE": new_role.NOMBRE,
            "PERMISOS": new_role.PERMISOS
        }

@app.post("/permiso", status_code=status.HTTP_201_CREATED)
def create(permiso: schemas.permiso = Body(default=None), db: Session = Depends(database.get_db)):
    if not permiso:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not permiso.nombre or not permiso.estado:
        return utility.get_json_response('E400', 'El nombre y el estado es obligatorio')
    else:
        new_permiso: models.permiso = tasks.createPermiso(db=db, permiso=permiso)
        return {
            "ID": new_permiso.ID,
            "NOMBRE": new_permiso.NOMBRE,
            "ESTADO": new_permiso.ESTADO
        }

@app.post("/role/{role_id}/permisos" , status_code=status.HTTP_201_CREATED)
def associate_permiso_to_role(role_id:int, permisos: schemas.PermisoUpdate = Body(default=None) , db: Session = Depends(database.get_db)):
    role = db.query(role).filter(role.ID == role_id).first()
    if not role:
        return utility.get_json_response('E404', 'El rol no existe')
    elif not permisos:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    else:
        new_role_permisos = models.role = tasks.associatePermisosToRole(db=db, role=role, permisos=permisos)
        return {
            "ID": new_role_permisos.ID,
            "NOMBRE":new_role_permisos.NOMBRE,
            "PERMISOS":new_role_permisos.PERMISOS
        }
@app.get("/role/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.delete("/role/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db(db=db)
    return {"msg": "Todos los roles y permisos fueron eliminados"}
