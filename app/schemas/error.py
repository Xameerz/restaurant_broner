from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    detail: str
    errors: Optional[List[ErrorDetail]] = None
    status_code: int
    code: Optional[str] = None 