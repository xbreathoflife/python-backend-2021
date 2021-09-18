from pydantic import BaseModel


class File(BaseModel):
    filename: str
    size: float
    is_archived: bool
