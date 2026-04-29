from fastapi.responses import JSONResponse
from fastapi import status

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": data,
        },
    )

def error_response(message="Error", status_code=status.HTTP_400_BAD_REQUEST):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": None,
        },
    )