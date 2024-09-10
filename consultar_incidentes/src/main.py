from fastapi import FastAPI, status

app = FastAPI()


@app.get("/ping", status_code=status.HTTP_200_OK)
def verify_health_incidentes():
    return {"msg": "Pong"}
