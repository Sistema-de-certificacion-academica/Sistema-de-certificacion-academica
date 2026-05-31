from datetime import datetime, timezone

def error_response(status_code: int, message: str, error_code: str, 
                   details: str, intentos_restantes: int = None,
                   sugerencia: str = None) -> dict:
    error = {
        "error_code": error_code,
        "details": details,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    if intentos_restantes is not None:
        error["intentos_restantes"] = intentos_restantes
    if sugerencia:
        error["sugerencia"] = sugerencia
    return {
        "success": False,
        "statusCode": status_code,
        "message": message,
        "error": error
    }

def success_response(status_code: int, message: str, data) -> dict:
    return {
        "success": True,
        "statusCode": status_code,
        "message": message,
        "data": data
    }

