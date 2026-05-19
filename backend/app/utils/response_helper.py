from fastapi.responses import JSONResponse


def success_response(data):
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": data
        }
    )


def error_response(message, status_code=500):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": message
        }
    )
