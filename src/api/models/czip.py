from pydantic import BaseModel
from typing import Optional


class InputData(BaseModel):
    currency: str
    when: Optional[str] = None
