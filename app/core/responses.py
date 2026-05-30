from datetime import datetime, timezone

def error_response(status_code: int, message: str, error_code: str, details: str) -> dict:
    return {
        "success": False,
        "statusCode": status_code,
        "message": message,
        "error": {
            "error_code": error_code,
            "details": details,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }

def success_response(status_code: int, message: str, data) -> dict:
    return {
        "success": True,
        "statusCode": status_code,
        "message": message,
        "data": data
    }