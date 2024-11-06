import enum
from fastapi.responses import JSONResponse
from fastapi import status


def get_json_response(error: str, msg: str) -> JSONResponse:
    class estatusErrorsCode(enum.Enum):
        E400 = status.HTTP_400_BAD_REQUEST
        E401 = status.HTTP_401_UNAUTHORIZED
        E403 = status.HTTP_403_FORBIDDEN
        E404 = status.HTTP_404_NOT_FOUND
        E412 = status.HTTP_412_PRECONDITION_FAILED
        E422 = status.HTTP_422_UNPROCESSABLE_ENTITY

    class estatusErrorsMsg(enum.Enum):
        E400 = 'Bad Request'
        E401 = 'Unauthorized'
        E403 = 'Forbidden'
        E404 = 'Not Found'
        E412 = 'Precondition Failed'
        E422 = 'Unprocessable Entity'

    return JSONResponse(
        status_code=estatusErrorsCode[error].value,
        content={
            "statusCode": estatusErrorsCode[error].value,
            "message": msg.upper(),
            "error": estatusErrorsMsg[error].value
        },
    )
