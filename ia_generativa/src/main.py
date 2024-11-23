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

@app.get("/iagenerativa/ping", status_code=status.HTTP_200_OK)
def verify_health():
    return {"msg": "Pong"}


@app.post("/ia/generativa", status_code=status.HTTP_201_CREATED)
def generate(description: str):
    if not description:
        return utility.get_json_response('E422', 'La descripcion es boligatoria')
    else:
        respuesta:str= tasks.generar_respuesta(description)
        return {
            "respuesta": respuesta
        }



