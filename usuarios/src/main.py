from dotenv import find_dotenv, load_dotenv
from fastapi import Body, FastAPI, status, Depends, Header
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from operator import itemgetter
from typing_extensions import Annotated
from typing import Union

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


@app.post("/usuario/register", status_code=status.HTTP_201_CREATED)
def create_users(user: schemas.UserRegister = Body(default=None), db: Session = Depends(database.get_db)):
    if not user:
        return utility.get_json_response('E422', 'El body de la petición esta vacio')
    elif not user.email or not user.username or not user.nombres or not user.apellidos or not user.password:
        return utility.get_json_response('E400', 'email, username, nombres, apellidos y password son campos obligatorios')
    else:
        email = user.email
        username = user.username
        user_db = tasks.verify_if_user_already_exist(db=db, email=email, username=username)

        if user_db:
            return utility.get_json_response('E412', 'Este usuario ya existe con este username y/o email')
        else:
            user, token = itemgetter('user', 'token')(tasks.create_user(db=db, user=user))
            return {
                "id": user.ID,
                "email": user.EMAIL,
                "username": user.USERNAME,
                "nombres": user.NOMBRES,
                "apellidos": user.APELLIDOS,
                "token": token,
            }


@app.get("/usuario/check-status", status_code=status.HTTP_200_OK)
def check_status(Authorization: Annotated[Union[str, None], Header()] = None, db: Session = Depends(database.get_db)):
    if not Authorization:
        return utility.get_json_response('E403', 'El token no fue suministrado en el header')
    else:
        given_token = Authorization.replace("Bearer", "").strip()
        user, is_old_one = itemgetter('user', 'is_old_one')(tasks.verify_token(token=given_token))
        if not is_old_one:
            user_db = tasks.get_user_active(db=db, email=user["email"], username=user["username"])
            new_token = tasks.get_access_token(email=user["email"], username=user["username"])
            return {
                "id": user_db.ID,
                "email": user_db.EMAIL,
                "username": user_db.USERNAME,
                "nombres": user_db.NOMBRES,
                "apellidos": user_db.APELLIDOS,
                "token": new_token,
            }
        else:
            user_db = tasks.get_user_active(db=db, email=user["email"], username=user["username"])
            return {
                "id": user_db.ID,
                "email": user_db.EMAIL,
                "username": user_db.USERNAME,
                "nombres": user_db.NOMBRES,
                "apellidos": user_db.APELLIDOS,
                "token": given_token,
            }


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
                token = tasks.get_access_token(email=user.EMAIL, username=user.USERNAME)
                return {
                    "id": user.ID,
                    "email": user.EMAIL,
                    "username": user.USERNAME,
                    "nombres": user.NOMBRES,
                    "apellidos": user.APELLIDOS,
                    "token": token,
                }


@app.get("/usuario/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return "pong"


@app.post("/usuario/reset", status_code=status.HTTP_200_OK)
def reset(db: Session = Depends(database.get_db)):
    tasks.reset_db(db=db)
    return {"msg": "Todos los usuarios fueron eliminados"}
