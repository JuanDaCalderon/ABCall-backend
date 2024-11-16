from fastapi import FastAPI, status
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/chatbot/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.post("/chatbot", status_code=status.HTTP_201_CREATED)
def generate(opcion: str):
    if not opcion:
        return utility.get_json_response('E422', 'La opcion es boligatoria')
    else:
        respuesta:str= tasks.generar_respuesta(opcion)
        return {
            "respuesta": respuesta
        }



