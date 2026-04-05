from pydantic import BaseModel, Field
from typing import Optional

class RewriteQueryRequest(BaseModel):
    query: str = Field(min_length=1)
