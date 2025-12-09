from pydantic import BaseModel
from typing import Any

class QueryRequest(BaseModel):
    query: str

class QueryResult(BaseModel):
    rows: list[dict[str, Any]]
    sql: str

class UserInfo(BaseModel):
    username: str
    role: str