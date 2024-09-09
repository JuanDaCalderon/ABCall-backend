import uvicorn
from typing import Union
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/ping", status_code=status.HTTP_200_OK)
def verify_health_incidentes():
    return {"msg": "Pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
