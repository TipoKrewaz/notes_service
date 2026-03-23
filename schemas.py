from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    data: str = Field(..., min_length=1, description="Свободная запись")


class Note(BaseModel):
    note_id: str
    data: str
