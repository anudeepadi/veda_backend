from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from config import API_KEY

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key_header: str = Depends(API_KEY_HEADER)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return api_key_header