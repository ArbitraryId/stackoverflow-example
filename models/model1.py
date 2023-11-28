from typing import Optional

from pydantic import BaseModel
from models.enums import Enum1

class Model(BaseModel):
    enum_field: Optional[Enum1] = None
